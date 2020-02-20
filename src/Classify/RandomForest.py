from src.Classify.Classifier import Classifier
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib

SCALERFILE = "models/rfc_scaler.J"
MODELFILE = "models/rfc_model.J"

class RandomForest(Classifier):
    def __init__(self,  X_train, y_train, scaling_function=StandardScaler, initial_weights='balanced', C=1):
        self.scaler = scaling_function()
        X_scaled = self.scaler.fit_transform(X_train)

        # save the model to disk so that it persists for production use
        joblib.dump(self.scaler, open(SCALERFILE, 'wb'))

        # Random Forest Classifier does not accept a regularization parameter
        self.model = RandomForestClassifier(class_weight=initial_weights)
        self.model .fit(X_scaled, y_train)

        # save the model to disk
        joblib.dump(self.model , open(MODELFILE, 'wb'))
