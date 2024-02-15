import shap

# TODO: This whole file, lol

# Feature ranking stuff with shap, not sure if it works, can't render stupid html 
# init the JS visualization code
shap.initjs()

# we use the first 100 training examples as our background dataset to integrate over
explainer = shap.DeepExplainer(knn.get_model(), X_train[:100])

# explain the first 10 predictions
# explaining each prediction requires 2 * background dataset size runs
shap_values = explainer.shap_values(X_test[:10])

# plot the explanation of the first prediction
# Note the model is "multi-output" because it is rank-2 but only has one column
shap.force_plot(explainer.expected_value[0], shap_values[0][0,:], X_test[0])