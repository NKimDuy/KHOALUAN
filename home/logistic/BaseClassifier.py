import time
from sklearn.linear_model import LogisticRegression
class BaseClassifier:
    def __init__(self, class_name, params={}):
        self.class_name = class_name
        self.params = params
        self.classifier = None

    def training(self, train_vectors, train_targets):
        start = time.time()
        self.classifier = globals()[self.class_name](**self.params)
        self.classifier.fit(train_vectors, train_targets)
        end = time.time()

        return {"duration": end - start}

    def predict(self, test_vectors):
        if self.classifier:
            predict = self.classifier.predict(test_vectors)
            return predict


class LogisticRegressionClassifier(BaseClassifier):
    def __init__(self, multi_class="ovr"):
        params = {
            "multi_class": multi_class,
            "solver": "lbfgs"
        }

        super().__init__(class_name=LogisticRegression.__name__,
                         params=params)