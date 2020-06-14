import numpy as np
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler

class svm_regression_modeler:

    def __init__(self, kernel='rbf', c=1e3, gamma=0.1, epsilon=0.00001):
        self.x_train = np.array(0)
        self.y_train = np.array(0)
        self.x_test = np.array(0)
        self.y_test = np.array(0)
        self.SVR = SVR(kernel=kernel, C=c, gamma=gamma, epsilon=epsilon)

        self.model = None

    # get 'x' column to be used in ML algorithm. returns [ [sentiment score day 1, 2, 3..] for each ticker ]
    # def rangeTo model_X(self, dfs, sentimentscores):
    #
    #     # create x column

    def buildModel(self, model_X, model_y, test_size=0.2):

        #pre-process data

        # scale X data
        rbX = RobustScaler()
        model_X = rbX.fit_transform(model_X)

        # print("pre-pocessed")
        # print(model_X)
        # print(model_y)

        # split data
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(model_X, model_y, test_size=test_size)

    def runModel(self, ):
        print("xt:", self.x_train, "yt:", self.y_train)
        self.model = self.SVR.fit(self.x_train, self.y_train)

        svm_confidence = self.SVR.score(self.x_test, self.y_test)
        print("svm confidence: ", svm_confidence)