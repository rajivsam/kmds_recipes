## Overview
This recipe illustrates how KMDS can be used to annotate your data. In some sub-domains, like image processing or natural language processing, there is explicit methodology and theory to segment data. For example, segmentation of images and part of speech tagging are standard tasks in these areas. In contrast, in business applications such as credit scoring, these annotations are usually developed as analysts understand the data or with the help of domain experts. Therefore, to have reproduciblity and maintainablity of developed models, it is critical to have the rationale and dependencies that motivated the creation of these annotaions. This is what KMDS can help with. In this recipe a lender quality annotation is added based on the modeling work done earlier. Therefore, the WOE modeling workflow is a dependency for this workflow.

To recap, the summary for lender data for 2023 is as follows:
1. There is a group of 12 K loans that are **gold quality**. There was no charge off events in lenders attributed to this group.
2. There is a group of about 3.5 K loans that have limited representation in the dataset. We cannot learn from these loans because we don't have sufficient data to evaluate generalization for supervised learning. Unsupervised modeling is probably a good candidate for this group. This is the _outlier_ group.
3. The remainder is what can be modeled with Weight of Evidence based featurization using a Logistic Regression model. The probabilities from this model is what is annotated in this workflow.

## Annotation Approach
1. The model from WOE modeling is saved to a model directory. In an enterprise setting this could be a _model registry_.
2. The saved model is loaded, and is used to score the 2023 data. This gives us the chargeoff probabilities for the entire dataset.
3. The probability calibration approach used _deciles_ to compute and compare estimated probability versus true probability. This binning scheme (deciles) produces many bins with low counts. This is because of the imabalance in the dataset (majority of the lenders will pay back in full). If we use this scheme, the resulting interpretation is a little too verbose and fine grained. So a quartile binning scheme was evaluated. This ameliorated the problem considerably. By combining the third and fourth bins together, we get a binning of the data with _similar_ counts in each bin. This gives us three bins. The interpretation is now very succinct. We can rate these bins as good, average and poor on the basis of the proportion of charge offs in each bin.
4. This annotation of the data into three grades, good, average and poor provides an interesting perspective on the quality levels of new lenders in 2024. If we take the view that we will approve those falling into bins 1 and 2, and every one falling into bin 3 is checked then we have an estimate of the risk we are accepting and the risk we are scrutinizing.
5. For details of implementation, please see [this notebook](https://github.com/rajivsam/kmds_recipes/blob/main/recipes/machine_learning/data_annotation/7a_loan_data_annotation.ipynb).

## KMDS Logging
1. WOE model is a dependency for this annotation workflow. This dependency must be indicated.
2. This is an application workflow because there is no experimentation involved, the computational approach to annotate the data is known apriori (just binning), so it is a _KnowledgeApplicationWorkflow_.
3. The drawback of the decile binning must be logged.
4. The quartile binning results must be logged.
5. The bin collapsing and the resulting bin structure with similar counts in each bin must be logged.
6. The summarization of the dataset into the three subsets, gold quality, outliers and WOE model scored, must be logged.
7. Please see [this notebook](https://github.com/rajivsam/kmds_recipes/blob/main/recipes/machine_learning/data_annotation/7a_chargeoffs_data_annotation_report.ipynb) for the KMDS report.

