## Overview
The setting for this recipe is as follows. You want to further your understanding of the 2023 7a data. You have decided to do deeper data analysis to develop better features (features that are interpretable directly in terms of business data as opposed to a model generated feature). This is a routine increment in most projects. Better decisions, better utilization of data comes from efforts to understand the fundamental characteristics of the data for your problem. This usually leads to better problem framing. 

In some application domains of machine learning, for example in Natural Language Processing (Part-Speech-Tagging), Image Processing (Image Segmentation), annotation of datasets is a full-fledged learning task with theory and research to provide guidelines. In applications of statistics or machine learning to business data, data annotation is usually done with domain expertise in the use case under consideration. The rationale and implementation guidelines in these cases must be well documented to be applied repeatedly. This is where KMDS can help.

## Key Ideas 

In this recipe, we look at the features in the 7a loans dataset more carefully and develop a set of concise features. These features are based on the following principles:
1. Generalization is an important aspect of machine learning. We cannot learn on subsets of data that do not let us evaluate the generalization of the learned hypothesis.
2. Categorical attributes with high branching (many categories) can limit generalization.
3. By examining the definition of the zip code attribute, we can feature engineer new attributes with less branching.

## Implementation
1. Please see [the wikipedia zipcode interpretation](https://en.wikipedia.org/wiki/ZIP_Code#:~:text=ZIP%20Codes%20are%20numbered%20with,delivery%20addresses%20within%20that%20region.). By limiting the zip code feature to the first three digits we can create category levels that offer us more data for learning with generalization.
2. Even after doing this, we still have a subset of data that have limited examples for learning. We set this aside as outliers (about 3.5 K records in dataset with about 23 K records). The larger pool of data, without the outliers, lends itself to developing models with generalization.
3. Weight of Evidence (for an explaination, see [this blog post](https://multithreaded.stitchfix.com/blog/2015/08/13/weight-of-evidence/) for example), is a very commonly used technique in risk assesment, especially in credit risk applications. Score cards based on this idea are very commonly used. The _category encoders_ package offers a _weight of evidence encoder_ to encode variables based on weight of evidence. 

## KMDS Logging
1. We are going to be analyzing the data and then use a fixed computational procedure to encode the cleaned data. So in keeping with [the guideline](https://github.com/rajivsam/KMDS/blob/main/feature_documentation/km_app_pipeline.md), a _KnowledgeApplicationWorkflow_ is created.
2. The goal of this workflow is to develop a clean and concise data representation for learning. Therefore, all observations are going to _DataRepresentationObservations_.
3. Feature engineering rationale and decisions are logged.
4. Outlier information is logged.
5. Weight of Evidence encoding is applied encode the cleaned data, this is logged.
Please see the notebook for details of the implementation.