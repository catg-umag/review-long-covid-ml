import sys

import numpy as np
import pandas as pd
from sklearn.ensemble import (
    AdaBoostRegressor,
    BaggingRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)

# for metrics
from sklearn.metrics import mean_squared_error, r2_score

# for check overfitting
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.neighbors import KNeighborsRegressor

# for training models
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor


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
    return response


# define the type of metrics
scoring = ["r2_score"]
keys = ["fit_time", "score_time", "test_score"]

k_fold_value = 10

df = pd.read_csv(sys.argv[1])
df = df.dropna()
name_export = sys.argv[2]

response = df["average"]
df_data = df.drop(columns=["average"])

X_train, X_test, y_train, y_test = train_test_split(
    df_data, response, test_size=0.3, random_state=42
)

print("Exploring Training predictive models")
matrix_data = []

print("Exploring SVR")
clf = SVR()
response = training_process(
    clf, X_train, y_train, X_test, y_test, scoring, k_fold_value, "SVR", keys
)
matrix_data.append(response)

print("Exploring KNN")
clf = KNeighborsRegressor()
response = training_process(
    clf, X_train, y_train, X_test, y_test, scoring, k_fold_value, "KNN", keys
)
matrix_data.append(response)


print("Exploring decision tree")
clf = DecisionTreeRegressor()
response = training_process(
    clf, X_train, y_train, X_test, y_test, scoring, k_fold_value, "DT", keys
)
matrix_data.append(response)

print("Exploring bagging method based DT")
clf = BaggingRegressor(n_jobs=-1)
response = training_process(
    clf, X_train, y_train, X_test, y_test, scoring, k_fold_value, "bagging", keys
)
matrix_data.append(response)


print("Exploring RF")
clf = RandomForestRegressor(n_jobs=-1)
response = training_process(
    clf, X_train, y_train, X_test, y_test, scoring, k_fold_value, "RF", keys
)
matrix_data.append(response)


print("Exploring Adaboost")
clf = AdaBoostRegressor()
response = training_process(
    clf, X_train, y_train, X_test, y_test, scoring, k_fold_value, "Adaboost", keys
)
matrix_data.append(response)


print("Exploring GradientTreeBoost")
clf = GradientBoostingRegressor()
response = training_process(
    clf,
    X_train,
    y_train,
    X_test,
    y_test,
    scoring,
    k_fold_value,
    "GradientBoostingRegressor",
    keys,
)
matrix_data.append(response)


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
