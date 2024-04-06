Model Development with Feature Engineering
------------------------------------------

This recipe develops a model using the WOE-encoded features and the data
representation developed in the feature engineering workflow. To recap,
this model is developed on the data after removing the gold-quality
loans and the outliers. The zip code is trimmed as discussed in the
earlier feature engineering post. This has the following consequences:
1. The imbalance is improved (from 5 percent charge-offs to about 11.4
percent charge-offs) 2. The cardinality of the feature space is reduced
considerably. 3. The dataset used for learning is smaller. The
attributes considered for featurization have good support from the
standpoint of evaluating generalization.

Modeling Approach
-----------------

1.  Logistic Regression is used to predict Charge Offs. The
    *scikit-learn* implementation is used. This offers the option to add
    regularization.
2.  (Weiss 2013) discusses the approaches to model development with
    imbalanced data. The evaluation metric is a key factor in the design
    and evaluation of classification models for imbalanced data. The
    preferred approach would be to develop an evaluation metric that
    considers the costs of correct and incorrect classification in the
    development and evaluation of the model. (Sheng and Ling 2006)
    provides a good summary and discussion of the main approaches used.
    If getting costs is not feasible, then the default evaluation
    technique is to use the ROC curve to tune the developed model for
    optimal performance. The key idea here is to use the probability of
    the event occurring (charge-offs, in this case) as the pivotal
    parameter to make the prediction. If the probability is below a
    threshold, the prediction is a non-event (paid in full), else we
    predict that the event will occur (charge off).
3.  There are some guidelines based on maximizing a statistic that would
    give us the maximum possible specificity and sensitivity - examples
    include geometric mean and Youden’s J statistic. These are
    guidelines developed using simulations or approximations in most
    cases. So they are a decent start, but you still may need to tune
    the threshold using a method that you can afford to evaluate. This
    could be as simple as a grid search or as sophisticated as Bayesian
    Optimization.
4.  Threshold moving involves evaluating model performance (recall and
    precision) over a range of threshold values and then determining an
    *acceptable* threshold, i.e., one that produces acceptable false
    positives and with desired sensitivity.
5.  The trade-off between an acceptable false positive rate (precision)
    and the desired sensitivity (recall) is a design issue that must be
    resolved in collaboration with the customer/business stakeholder.
    Therefore this is a business decision. The notebook evaluates the
    performance over a range of values. As is evident, at the end of the
    day, even taking the ROC curve approach rather than an explicit
    costs-based approach (for example, one that considers
    misclassification costs), we will face the problem of deciding
    between the acceptable false positive rate and the desired
    sensitivity. So, in my view, it is always better to start the cost
    conversation early in imbalance problems. What is acceptable depends
    on the application domain. In a healthcare setting where we want to
    avoid expensive investigations, false positives are bad. In a credit
    risk or security setting, some level of false positives may be
    acceptable, the sensitivity is very critical.
6.  The Precision Recall curve summarizes the performance of the model
    with respect to these parameters. It is provided in the notebook
7.  This notebook depends on the feature engineering and WOE encoding
    done in the feature engineering workflow. So the dependency between
    the model workflow and the feature engineering workflow must be
    captured.
8.  The probability of an event is a critical input in prediction. We
    want accurate probabilities. A probability calibration curve can
    give us the *reliability* of the probabilities obtained from the
    model. The calibration curve contrasts the predicted and true
    probabilities.
9.  There are techniques to recalibrate the probabilities from the
    model. These methods try to correct the model probability to match
    the true probability. A recalibration method is evaluated in the
    model (Isotonic Regression.) development notebook.
10. Due to the class imbalance, most of the model probabilities will be
    low values. So a histogram of the model probabilities and the
    recalibrated probabilities will exhibit a power law type
    distribution, with most of the mass being associated with low
    values. This is illustrated in the notebook.
11. The notebook containing the WOE modeling implementation is
    `here <https://github.com/rajivsam/kmds_recipes/blob/main/recipes/machine_learning/imbalanced_cost_based_learning/WOE_modeling.ipynb>`__

KMDS Logging
------------

1. We are only going to consider a single modeling approach, so the
   workflow type is going to be *KnowledgeApplicationWorkflow*.
2. The model selection option is going to be Logistic Regression, this
   is logged as a *ModelSelectionObservation*.
3. The modelling choice here is going to be to select the regularization
   parameter using 5 fold cross validation. This is logged.
4. The model calibration choice is going to be *isotonic regression*.
   This is logged as modelling choice.
5. The threshold that maximizes the *geometric mean* of the product of
   *sensitivity* and *specificity* is going to be used as the starting
   point to explore *threshold moving*. This is logged as a modelling
   choice.
6. The interval that is explored as part of threshold moving is logged.
7. The *sba_7a_loans_WOE_DR.xml* is the feature engineering workflow
   this workflow depends on. This is logged.
8. The report is run on the knowledge base in a manner similar to other
   cases. A convinience method to report the dependent workflow in a
   manner similar to other observations will be added very soon to KMDS.

References
----------

.. container:: references csl-bib-body hanging-indent
   :name: refs

   .. container:: csl-entry
      :name: ref-elkan2001foundations

      Elkan, Charles. 2001. “The Foundations of Cost-Sensitive
      Learning.” In *International Joint Conference on Artificial
      Intelligence*, 17:973–78. 1. Lawrence Erlbaum Associates Ltd.

   .. container:: csl-entry
      :name: ref-leborgne2022fraud

      Le Borgne, Yann-Aël, Wissam Siblini, Bertrand Lebichot, and
      Gianluca Bontempi. 2022. *Reproducible Machine Learning for Credit
      Card Fraud Detection - Practical Handbook*. Université Libre de
      Bruxelles.
      https://github.com/Fraud-Detection-Handbook/fraud-detection-handbook.

   .. container:: csl-entry
      :name: ref-imblearnref

      Lemaître, Guillaume, Fernando Nogueira, and Christos K. Aridas.
      2017. “Imbalanced-Learn: A Python Toolbox to Tackle the Curse of
      Imbalanced Datasets in Machine Learning.” *Journal of Machine
      Learning Research* 18 (17): 1–5.
      http://jmlr.org/papers/v18/16-365.html.

   .. container:: csl-entry
      :name: ref-seiffert2009rusboost

      Seiffert, Chris, Taghi M Khoshgoftaar, Jason Van Hulse, and Amri
      Napolitano. 2009. “RUSBoost: A Hybrid Approach to Alleviating
      Class Imbalance.” *IEEE Transactions on Systems, Man, and
      Cybernetics-Part A: Systems and Humans* 40 (1): 185–97.

   .. container:: csl-entry
      :name: ref-sheng2006thresholding

      Sheng, Victor S, and Charles X Ling. 2006. “Thresholding for
      Making Classifiers Cost-Sensitive.” In *Aaai*, 6:476–81.

   .. container:: csl-entry
      :name: ref-weiss2013foundations

      Weiss, Gary M. 2013. “Foundations of Imbalanced Learning.”
      *Imbalanced Learning: Foundations, Algorithms, and Applications*,
      13–41.
      https://storm.cis.fordham.edu/gweiss/papers/foundations-imbalanced-13.pdf.
