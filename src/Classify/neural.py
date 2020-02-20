import numpy as np
import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from  tensorflow.keras.initializers import Constant

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from keras.losses import BinaryCrossentropy
from keras import metrics
import joblib

def buildNN(good_cases, bad_cases):
	bias = np.log([bad_cases / good_cases])
	output_bias = Constant(bias)
	nn = Sequential()
	#nn.add(Dense(50, input_dim=170, activation='relu'))
	#nn.add(Dropout(0.2))
	nn.add(Dense(25, activation='relu'))
	nn.add(Dropout(0.5))
	nn.add(Dense(1, activation='sigmoid', bias_initializer=output_bias))
	# Compile model
	nn.compile(loss=BinaryCrossentropy(), optimizer=Adam(lr=0.01),
			   metrics=[
				   		metrics.BinaryAccuracy(name='accuracy'),
						metrics.Precision(name='precision'),
						metrics.Recall(name='recall'),])
	return nn

# Create a dataframe from the training set
dfTrain = pd.read_csv("data/aps_failure_training_set.csv")

# Create the input set by removing the output label column
X = dfTrain.drop('class', axis=1)

# Replace missing inputs by averaging the other values
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
imputer.fit(X)
X = imputer.transform(X)

# Create training and validation sets from so the model can be fit, then tested on new data
X_train, X_test, y_train, y_test = train_test_split(X, dfTrain['class'], test_size=0.20)

# Scale the input values. Scaled and normalized inputs optimize better
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)
joblib.dump(scaler, open('models/nn_scaler.J', 'wb'))

# encode class values as integers
encoder = LabelEncoder()
encoder.fit(y_train)
y_enc = encoder.transform(y_train)

# Display the frequency of each class in the training set
number_work, number_fail = np.bincount(y_enc)
print (number_work, number_fail)

y_enctest = encoder.transform(y_test)

# compile the keras model and fit to input data
nn = buildNN(number_work, number_fail)
nn.fit(X_scaled, y_enc, epochs=50, batch_size=64)
# save the model to disk
joblib.dump(nn, open('models/nn.J', 'wb'))

# evaluate the model
_, train_acc, train_prec, train_recall = nn.evaluate(X_train, y_enc, verbose=0)
_, test_acc, test_prec, test_recall = nn.evaluate(X_test, y_enctest, verbose=0)
print('Accuracy: Train = {0:.3f}, Test = {1:.3f}'.format(train_acc, test_acc))
