import numpy as np
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import GridSearchCV

class svm_regression_modeler:

    def __init__(self, kernel='rbf', c=1e3, gamma=0.1, epsilon=0.00001):
        self.x_train = np.array(0)
        self.y_train = np.array(0)
        self.x_test = np.array(0)
        self.y_test = np.array(0)
        self.SVR = SVR(kernel=kernel, C=c, gamma=gamma, epsilon=epsilon)

        # optimization parameters
        self.c_range, self.gam_range, self.folds = [], [], []

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

    def runModel(self):
        # print("xt:", self.x_train, "yt:", self.y_train)
        self.model = self.SVR.fit(self.x_train, self.y_train)

        svm_confidence = self.SVR.score(self.x_test, self.y_test)
        print("initial svm confidence: ", svm_confidence)

    def optimize(self):

        # print(self.x_train, self.y_train)

        folds = int(np.sqrt(self.folds//3))

        c_params = np.linspace(self.c_range[0], self.c_range[1], folds)

        gam_params = np.linspace(self.gam_range[1], self.c_range[0], folds)

        param_grid = {'C': c_params, 'gamma': gam_params, 'kernel': ['rbf', 'poly', 'sigmoid']}

        # print(c_params, gam_params, param_grid)

        print("grid refitting...")

        grid = GridSearchCV(self.SVR, param_grid, refit=True, verbose=2)
        grid.fit(self.x_train, self.y_train)

        grid_predictions = grid.predict(self.x_test)
        print("grid predictions:", grid_predictions)

        print(grid.best_estimator_)

        print(self.SVR.score(self.x_test, self.y_test))

    # loads optimization parameters from a file
    def loadOpFile(self, path):

        opfile = open(path, 'r')

        self.c_range = [float(i) for i in opfile.readline().split()]

        self.gam_range = [float(i) for i in opfile.readline().split()]

        self.folds = int(opfile.readline())

        opfile.close()

        print("loaded optimization profile:", path)

    # help user optimize data
    def opWizard(self):
        print("welcome to the model optimization wizard")
        c1 = input("input C (regularisation parameter)\nlower bound (suggested is 0.001: ")
        print("")
        c2 = input("input C (regularisation parameter)\nupper bound (sugguested is 100):")
        print("")
        g1 = input("input γ (separation sentitivity parameter)\nlower bound (suggested is 1e-10: ")
        print("")
        g2 = input("input γ (separation parameter)\nupper bound (sugguested is 0.1):")
        print("")
        self.folds = input("input folds (higher folds -> higher resolution -> higher processing timme (recommended: 300):")

        self.c_range, self.gam_range = [c1, c2], [g1, g2]


# m = svm_regression_modeler()
# m.loadOpFile('profile1.otmp')
# m.opWizard()