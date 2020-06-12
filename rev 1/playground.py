import pandas as pd
import numpy as np
import time
import datetime
import os

# custom classes
from twitterDataRetriever import twitterDataRetriever as TDR
from sentimentCalculator import sentimentCalculator as SC
from stockDataRetriever import stockDataRetriever
from svm_regression_modeler import svm_regression_model

os.remove("out.txt")

tdr = TDR()
sc = SC()

quantity = 1000

date_step = datetime.timedelta(days=1)

startDate = (datetime.date(2020, 6, 3))
endDate = (datetime.date(2020, 6, 10))

print(startDate, endDate)
# startDate =  "2020-06-05"
# endDate = "2020-06-06"

#terms = ['$MSFT', '$AAPL', '$F', '$AMD', '$AMZN']#'$NVDA', '$SHOP',
         #'$ETSY', '$SQ', '$SPY', '$WORK', '$T', '$IBM', '$BAM']

terms = ["$AMD"]#, '$MDT', '$MPW', '$BAM', '$OGI', '$AKTS', '$GE', '$BABA', '$ACB', '$AAPL', '$F', '$AMD', '$AMZN', '$NVDA', '$SHOP', '$ETSY', '$SQ', '$SPY', '$WORK', '$T', '$IBM', '$BAM']

print("Start date: ", str(startDate), "\nEnd date: ", endDate)
print("search quantity:", quantity)

t0 = time.time()

rangeArray = tdr.retrieveRangeByTerm(terms.copy(), str(startDate), str(endDate), date_step, quantity, ignoreRetweents=False)

print("fetching elapsed time: ", time.time() - t0)
#print(rangeArray)

t0 = time.time()

#print("getting tweets....")
# tweetdfs = tdr.retrieveByTerm(terms.copy(), startDate, endDate, quantity)
# for df in tweetdfs:
#     print(df.loc[:, :])

# cleanup tweets
# each ticker in twRangeDate
day = 0

msft_stScores = []

# load sentiment data and create reference df
sc.loadSentimentData()


# index sentiment scores
for dflist in rangeArray:

    day+=1

    #print("\nDay " + str(day) + ": \n")

    tdr.cleanupTweetData(dflist, disQSpammedTags=False)

    sentimentScores = sc.calculateSentiment(dflist)
    #print(sentimentScores)

    for i, score in enumerate(sentimentScores):
        print("sentiment score for " + terms[i] + " over " + str(quantity) + " datapoints: " + str(score))

        msft_stScores.append(float(score))

    best_buy = terms[sentimentScores.index(max(sentimentScores))]
    best_sell = terms[sentimentScores.index(min(sentimentScores))]
    # print("best buy: " + best_buy)
    # print("best sell: " + best_sell)

    print("processing elapsed time: ", time.time() - t0)


print(msft_stScores)

# get stock data
s = stockDataRetriever()

d = []

for term in terms:

    data = s.retrieveData(term[1:], "7d", "1d")
    print("data1: ", data)

    print("df: ", data)

    s.parseData(data, ['Open', 'Close'])
    print("data2:", data)

    d.append(data)

print(d)

# still hard coded
deltas = s.getDeltas(d[0])
print("deltas:", deltas)

print(msft_stScores)
MLX = msft_stScores
MLY = deltas
print(MLY)

model_X = []
model_y = []

for entry in MLX:
    model_X.append([entry, deltas[MLX.index(entry)]])

model_X = (np.array(model_X[:6]).reshape(6, 2))

model_y = np.array(MLY[1:7])

print("X:", model_X, "\n\nY:", model_y[:6])

# SVM modeler
sv_model = svm_regression_model()#'rbf', 10, 100)

print(model_X.shape, model_y.shape)

sv_model.buildModel(model_X, model_y, 0.2)
sv_model.runModel()

print("predicting over X =", np.array([[MLX[-1], deltas[-1]]]))

svm_prediction = sv_model.SVR.predict(np.array([[MLX[-1], deltas[-1]]]))
print("predicted value: ", svm_prediction)