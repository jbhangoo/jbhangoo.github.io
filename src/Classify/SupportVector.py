from src.Classify.Classifier import Classifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import joblib

SCALERFILE = "models/svc_scaler.J"
MODELFILE = "models/svc_model.J"

class SupportVector(Classifier):
    def __init__(self, X_train, y_train, scaling_function=StandardScaler, initial_weights='balanced', C=1):
        self.scaler = scaling_function()
        X_scaled = self.scaler.fit_transform(X_train)

        # save the model to disk so that it persists for production use
        joblib.dump(self.scaler, open(SCALERFILE, 'wb'))

        self.model = SVC(class_weight=initial_weights, C=C)
        self.model .fit(X_scaled, y_train)

        # save the model to disk
        joblib.dump(self.model , open(MODELFILE, 'wb'))
