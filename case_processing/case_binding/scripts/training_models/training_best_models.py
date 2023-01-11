import sys

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# for metrics
from sklearn.metrics import mean_squared_error, r2_score

# for check overfitting
from sklearn.model_selection import cross_validate, train_test_split


# function to obtain metrics using the testing dataset
def get_performances(description, predict_label, real_label):
    r2_score_value = r2_score(real_label, predict_label)
    mean_squared_error_value = mean_squared_error(real_label, predict_label)

    row = [description, r2_score_value, mean_squared_error_value]
    return row


# function to process average performance in cross val training process
def process_performance_cross_val(performances, keys):

    row_response = []
    for i in range(len(keys)):
        value = np.mean(performances[keys[i]])
        row_response.append(value)
    return row_response


# function to train a predictive model
def training_process(
    model, X_train, y_train, X_test, y_test, scores, cv_value, description, keys
):
    print("Train model with cross validation")
    model.fit(X_train, y_train)
    response_cv = cross_validate(model, X_train, y_train, cv=cv_value)
    performances_cv = process_performance_cross_val(response_cv, keys)

    print("Predict responses and make evaluation")
    responses_prediction = clf.predict(X_test)
    response = get_performances(description, responses_prediction, y_test)
    response = response + performances_cv
    return response, responses_prediction


# define the type of metrics
scoring = ["r2_score"]
keys = ["fit_time", "score_time", "test_score"]

k_fold_value = 10

df = pd.read_csv(sys.argv[1])
df = df.dropna()
path_export = sys.argv[2]

response = df["average"]
df_data = df.drop(columns=["average"])

X_train, X_test, y_train, y_test = train_test_split(
    df_data, response, test_size=0.3, random_state=42
)

print("Exploring Training predictive models")
matrix_data = []

print("Exploring RF")
clf = RandomForestRegressor(n_jobs=-1)
response, responses_prediction = training_process(
    clf, X_train, y_train, X_test, y_test, scoring, k_fold_value, "RF", keys
)
matrix_data.append(response)

name_export = "{}summary_data.csv".format(path_export)
df_export = pd.DataFrame(
    matrix_data,
    columns=[
        "description",
        "test_r2_score",
        "test_mean_squared_error",
        "fit_time",
        "score_time",
        "train_test_score",
    ],
)
df_export.to_csv(name_export, index=False)

df_predictions = pd.DataFrame()
df_predictions["real"] = y_test
df_predictions["predictions"] = responses_prediction

name_export = "{}predictions_to_plot.csv".format(path_export)
df_predictions.to_csv(name_export, index=False)
