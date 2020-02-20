import numpy as np
import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

# Create a dataframe from the test set
dfTest = pd.read_csv("data/aps_failure_test_set.csv")

# Create the input set by removing the output label column
X_test = dfTest.drop('class', axis=1)
y_test = dfTest['class']

# Replace missing inputs by averaging the other values
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
imputer.fit(X_test)
X_test = imputer.transform(X_test)

# Load the scaler the model was built with
scaler = joblib.load('models/xg_scaler.J')
X_test = scaler.transform(X_test)

# load the model from disk
rfc = joblib.load('models/xg.J')
y_pred = rfc.predict(X_test)

# Compute metrics of how the support vector machine performed
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(accuracy_score(y_test, y_pred))
