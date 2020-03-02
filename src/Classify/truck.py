import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from src.Classify.Classifier import Classifier
from src.Classify.SupportVector import SupportVector
from src.Classify.RandomForest import RandomForest
from src.Classify.NaiveBayes import NaiveBayes

def fillMissing(X):
    '''
    Replace missing inputs by averaging the other values for that attribute
    :param X:   data of input values with missing values
    :return:    data with missing values filled in
    '''
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    imputer.fit(X)
    X_filled = imputer.transform(X)
    return X_filled

def encodeLabels(y):
    '''
    Encode class values as integers
    :param y:   Vector of class labels
    :return:    Class labels encoded as integers
    '''
    encoder = LabelEncoder()
    encoder.fit(y)
    y_enc = encoder.transform(y)
    return y_enc

# Create input dataframe and output labels from the training set
dfTrain = pd.read_csv("data/aps_failure_training_set.csv")
X = dfTrain.drop('class', axis=1)
y = dfTrain['class']

# Replace missing inputs by averaging the other values for that attribute
X_train = fillMissing(X)

# Encode class labels
y_train = encodeLabels(y)

# Display the frequency of each class in the training set to show any class imbalances
category_counts = np.bincount(y_train)
print(category_counts)

#model = Classifier(X_train, y_train, initial_weights={0:1, 1:59}, C=0.1)
#model = SupportVector(X_train, y_train, initial_weights={0:1, 1:59}, C=0.01)
#model = RandomForest(X_train, y_train, initial_weights='balanced_subsample')
model = NaiveBayes(X_train, y_train, scaling_function=MinMaxScaler)

dfTest = pd.read_csv("data/aps_failure_test_set.csv")
X_test = dfTest.drop('class', axis=1)
y_test = dfTest['class']

# Replace missing inputs by averaging the other values for that attribute
X_filled = fillMissing(X_test)

# Encode class labels
y_enc = encodeLabels(y_test)

y_pred = model.predict(X_filled)
model.evaluateModel(y_enc, y_pred)
