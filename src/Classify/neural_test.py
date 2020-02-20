import numpy as np
import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

import joblib

def get_metrics(y_true, y_pred): #taken from old keras source code
    # accuracy: (tp + tn) / (p + n)
    accuracy = accuracy_score(y_pred, y_true)
    print('Accuracy: {:.3f}'.format(accuracy))
    # precision tp / (tp + fp)
    precision = precision_score(y_pred, y_true)
    print('Precision: {:.3f}'.format(precision))
    # recall: tp / (tp + fn)
    recall = recall_score(y_pred, y_true)
    print('Recall: {:.3f}'.format(recall))
    # f1: 2 tp / (2 tp + fp + fn)
    f1 = f1_score(y_pred, y_true)
    print('F1 score: {:.3f}'.format(f1))
    matrix = confusion_matrix(y_pred, y_true)
    print(matrix)

# Create a dataframe from the test set
dfTest = pd.read_csv("data/aps_failure_test_set.csv")

# Create the input set by removing the output label column
X_test = dfTest.drop('class', axis=1)
y_test = dfTest['class']

# encode class values as integers
encoder = LabelEncoder()
encoder.fit(y_test)
y_enc = encoder.transform(y_test)

# Replace missing inputs by averaging the other values
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
imputer.fit(X_test)
X_scaled = imputer.transform(X_test)

# Load the scaler the model was built with
scaler = joblib.load('models/nn_scaler.J')
X_test = scaler.transform(X_test)

# load the model from disk
nn = joblib.load('models/nn.J')

y_pred = nn.predict(X_scaled)
precision, recall, f1_val = get_metrics(y_enc, y_pred)

print(precision, recall, f1_val)

_, test_acc = nn.evaluate(X_scaled, y_enc, verbose=0)
print('Accuracy: {0:.3f}'.format(test_acc))
