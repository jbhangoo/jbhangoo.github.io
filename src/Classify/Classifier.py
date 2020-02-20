from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

SCALERFILE = "models/scaler.J"
MODELFILE = "models/model.J"

class Classifier:
    '''
    This is a basic logistic regression classifier. Use it as a base class for all classifiers.
    '''
    def __init__(self, X_train, y_train, scaling_function=StandardScaler, initial_weights='balanced', C=1):
        '''
        Base constructor sets file names for model and scaler persistence.
        Should override in subclass with more specific names

        Override this with the particular classifier for the subclass
        :param X_train: Training input data
        :param y_train: Training  output labels
        :param scaling_function: Transformation function to normalize input
        '''
        self.scaler = scaling_function()
        X_scaled = self.scaler.fit_transform(X_train)

        # save the model to disk so that it persists for production use
        joblib.dump(self.scaler, open(SCALERFILE, 'wb'))

        # Adjust the initial weights and regularization parameter as specified
        self.model = LogisticRegression(class_weight=initial_weights, C=C)
        self.model.fit(X_scaled, y_train)

        # save the model to disk for production use
        joblib.dump(self.model, open(MODELFILE, 'wb'))

    def predict(self, X):
        '''
        Use the classifier model to predict classes for given input
        scale by the same transform as the trainer
        :param X:   input data
        :return:    predicted output
        '''
        X_scaled = self.scaler.transform(X)
        y_pred = self.model.predict(X_scaled)
        return y_pred

    def evaluateModel(self, y_act, y_pred):
        '''
        Compute metrics of how the support vector machine performed
        :param y_act:   Actual labels
        :param y_pred:  Predicted output
        :return:
        '''
        print("Overall accuracy: {:.4f}".format(accuracy_score(y_act, y_pred)))
        print("\nConfusion Matrix")
        print(confusion_matrix(y_act, y_pred))
        print("\nDetailed Report")
        print(classification_report(y_act, y_pred))
