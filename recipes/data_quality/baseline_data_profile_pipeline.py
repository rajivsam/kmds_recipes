from prefect import flow, task
import pandas as pd
from kmds.utils.config_reader import get_config
import logging
from minio import Minio
import sys
from io import StringIO
from typing import List
from kmds.ontology.kmds_ontology import *
from kmds.tagging.tag_types import ExploratoryTags


@task(log_prints=True)
def load_data_from_bucket() ->pd.DataFrame:
    s3_cfg = get_config("../minio_config.yaml")
    HOST_URL = s3_cfg["HOST_URL"]
    ACCESS_KEY = s3_cfg["ACCESS_KEY"]
    SECRET_KEY = s3_cfg["SECRET_KEY"]
    try:
        client = Minio(HOST_URL, ACCESS_KEY, SECRET_KEY, secure=False)
        object_name = "incident_event_log_02.csv"
        obj = client.get_object(s3_cfg["BUCKET_NAME"], object_name)
        data = obj.data
        s = str(data,'utf-8')
        data = StringIO(s)
        df = pd.read_csv(data)
    except Exception as e:
        logging.error("Could not connect to S3 bucket, check connection information!")
        sys.exit(1)
    return df

@task(log_prints=True)
def profile_meta_information(df: pd.DataFrame) -> List[str]:
    meta_info = []
    f1 = "data file has {nr} rows and {nc} columns".format(nr=df.shape[0], nc=df.shape[1])
    meta_info.append(f1)
    data_types = df.dtypes
    for k,v in data_types.items():
        f = "column {c} is of type {t}".format(c=k, t=v)
        meta_info.append(f)

    return meta_info

@task(log_prints=True)
def profile_missing_values(df: pd.DataFrame) -> List[str]:
    missing_values = {c: df[c].isnull().sum() for c in df.columns.tolist() if  df[c].isnull().sum() > 0}
    missing_value_obs = ["{column} has {n} missing values".format(column=k, n=v) for k,v in missing_values.items()]

    return missing_value_obs

@task(log_prints=True)
def update_ontology(obs:List[str]) -> None:
    kaw = KnowledgeApplicationWorkflow("ITSM Raw Data Profile", namespace=onto)
    exp_obs_list = []
    observation_count :int = 1

    for o in obs:
        e = ExploratoryObservation(namespace=onto)
        e.finding = o
        e.finding_sequence = observation_count
        e.exploratory_observation_type = ExploratoryTags.DATA_QUALITY_OBSERVATION.value
        observation_count +=1
        exp_obs_list.append(e)
    
    kaw.has_exploratory_observations = exp_obs_list

    return




@task(log_prints=True)
def upload_report_to_bucket(onto: Ontology) ->None:
    s3_cfg = get_config("../minio_config.yaml")
    HOST_URL = s3_cfg["HOST_URL"]
    ACCESS_KEY = s3_cfg["ACCESS_KEY"]
    SECRET_KEY = s3_cfg["SECRET_KEY"]
    storage_path = "ITSM_Raw_Data_Profile.xml" 
    onto.save(file=storage_path, format="rdfxml")
    destination = "knowledge_representation" + "/" + storage_path
    try:
        client = Minio(HOST_URL, ACCESS_KEY, SECRET_KEY, secure=False)
        object_name = "incident_event_log_02.csv"
        obj = client.fput_object(s3_cfg["BUCKET_NAME"], destination, storage_path)
        logging.info("Uploaded profile file to bucket!")
    except Exception as e:
        logging.error("Could not connect to S3 bucket, check file details")
        sys.exit(1)



@flow(name="itsm_raw_datafile_profile")
def itsm_baseline_data_profile():
    df = load_data_from_bucket()
    mi = profile_meta_information(df)
    mv = profile_missing_values(df)
    obs = mi + mv
    update_ontology(obs)

    upload_report_to_bucket(onto=onto)


        
    return

# run the flow!
if __name__=="__main__":
    itsm_baseline_data_profile()

