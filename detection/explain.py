import shap

def explain(model, sample):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(sample)

    if isinstance(shap_values, list):
        vals = shap_values[1][0]
    else:
        vals = shap_values[0]

    importance = sorted(
        zip(sample.columns, vals),
        key=lambda x: abs(float(x[1])),
        reverse=True
    )

    return importance