from twitter import tweethandler
from stocks import stockDataHandler
from datetime import datetime, timedelta
from modeler import svm_regression_modeler
import numpy as np
import argparse
import matplotlib.pyplot as plt

def main(start_date, exclude, training, quantity):

    # get stock data
    sdh = stockDataHandler()

    tickers = ['$SPY']
    #start_date = datetime(2020, 6, 2, 0, 0, 0)

    print("retrieving stock data...")

    stockData  = sdh.handleStockData(tickers, start_date)
    print(stockData)

    # get tweet data
    tw = tweethandler()

    print("retrieving", quantity*(datetime.now()-start_date).days, "tweets.. ")

    scores = tw.get_cell_st_scores("$SPY", start_date, datetime.today(), quantity)

    print("building model...")

    # prepare data to hand to model
    model_x1 = scores
    print(model_x1)
    model_x2 = stockData[0]

    model_X = []

    for i, entry in enumerate(model_x1[:exclude]):
        model_X.append([entry, model_x2[i]])

    model_X = np.array(model_X).reshape(len(model_X), 2)

    model_y = np.array(model_x2[1:(exclude+1)])

    print(model_X)
    print(model_y)

    #SVM modeler
    sv_model = svm_regression_modeler(kernel='rbf', c=1e2, gamma=1e-3)

    sv_model.buildModel(model_X, model_y, training)
    sv_model.runModel()

    # predict remaining datapoints
    svm_predictions = []
    scores_remaining = []

    for i, score_reminaing in enumerate(model_x1[exclude:]):

        predict_data = np.array([score_reminaing, model_x2[i]]).reshape(1, -1)
        print("using", predict_data, "to predict")
        svm_prediction = sv_model.SVR.predict(predict_data)
        svm_predictions.append(svm_prediction)
        scores_remaining.append(score_reminaing)
        print("prediction for", (datetime.now()-(i*timedelta(1)), score_reminaing))
        print(svm_prediction)

    xplt1 = [i for i in range(len(model_x2))]
    xplt2 = [i+len(xplt1) for i in range(len(svm_predictions))]

    print(xplt2)

    # plot data
    plt.plot([i for i in range(len(model_x2))], model_x2, 'ro', xplt2, svm_predictions, 'bs')
    plt.axis([0, (datetime.today()-start_date).days, -0.08, 0.08])
    plt.show()


# Handle arguments
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--training', default=0.8,
                    help='percentage of data to use for training')
parser.add_argument('--start_date', default="2020-01-01",
                    help='start date, format yyyy-mm-dd')
parser.add_argument('--exclude', default=2,
                    help='number of datapoints from top of calender tree to exclude')
parser.add_argument('--tweet_quantity', default=500,
                    help='number of tweets to gather per cell')

args = parser.parse_args()
start_date = datetime.strptime(args.start_date, "%Y-%m-%d")

exclude = int(args.exclude)*-1

training = round(1 - float(args.training), 2)

quantity = int(args.tweet_quantity)

print(start_date, training, quantity)

main(start_date, exclude, training, quantity)