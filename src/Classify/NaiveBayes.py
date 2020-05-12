from src.Classify.Classifier import Classifier
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
import joblib

SCALERFILE = "models/nb_scaler.J"
MODELFILE = "models/nb_model.J"

class NaiveBayes(Classifier):
    def __init__(self,  X_train, y_train, scaling_function=StandardScaler, initial_weights='balanced', C=1):
        self.scaler = scaling_function()
        X_scaled = self.scaler.fit_transform(X_train)

        # save the model to disk so that it persists for production use
        joblib.dump(self.scaler, open(SCALERFILE, 'wb'))

        # Complement Naive Bayes does not nake the assumptions of the Multinomial model. Turn off smoothing.
        self.model = GaussianNB()
        self.model .fit(X_scaled, y_train)

        # save the model to disk
        joblib.dump(self.model , open(MODELFILE, 'wb'))
