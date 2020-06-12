import pandas as pd
import numpy as np
import sys

class sentimentCalculator:

    def __init__(self):

        # path to sentiment dictionary files
        # mac
        if sys.platform == "darwin":

            self.positiveWordsSrc = ["/Users/gabrielruoff/Dropbox/Stocks/StockOCAnalyzer/resources/opinion-lexicon-English/positive-words.txt"]
            self.negativeWordsSrc = ["/Users/gabrielruoff/Dropbox/Stocks/StockOCAnalyzer/resources/opinion-lexicon-English/negative-words.txt"]

        else:

            # windows
            self.positiveWordsSrc = ["C:/Users/GEruo/Dropbox/Stocks/StockOCAnalyzer/resources/opinion-lexicon-English/positive-words.txt",
                                     "C:/Users/GEruo/Dropbox/Stocks/StockOCAnalyzer/resources/subjclueslen-dict/negative.txt"]

            self.negativeWordsSrc = ["C:/Users/GEruo/Dropbox/Stocks/StockOCAnalyzer/resources/opinion-lexicon-English/negative-words.txt",
                                     "C:/Users/GEruo/Dropbox/Stocks/StockOCAnalyzer/resources/subjclueslen-dict/negative.txt"]

        self.positiveWordsar = []
        self.negativeWordsar = []

        self.sentimentdf = None
        self.sentimentdfindexref = None

        # pandas options
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 100)
        pd.set_option('display.max_colwidth', None)

    def loadSentimentData(self):

        # load positive words
        for wordList in self.positiveWordsSrc:

            file = open(wordList, encoding="ISO-8859-1")

            for line in file:

                if line.__contains__(";"):

                    pass

                else:

                    self.positiveWordsar.append(line.rstrip())

            file.close()

        # load negative words
        for wordList in self.negativeWordsSrc:

            file = open(wordList, encoding="ISO-8859-1")

            for line in file:

                if line.__contains__(";"):

                    pass

                else:

                    self.negativeWordsar.append(line.rstrip())

            file.close()

        self.sentimentdfindexref = self.positiveWordsar + self.negativeWordsar

        # print number of loaded words
        print("loaded " + str(len(self.sentimentdfindexref)) + " words into dictionary")
        print(str(len(self.positiveWordsar)), " positive words, ", str(len(self.negativeWordsar)), " negative words")

        # build row array for dataframe
        columns = ['word', 'instances', 'refscore']

        df = [[word, 0, 5] for word in self.positiveWordsar] + [[word, 0, -5] for word in self.negativeWordsar]

        # build dataframe from array
        df = pd.DataFrame(data=np.array(df), columns=columns)

        # convert columns to integers
        df['instances'] = df['instances'].astype(int)
        df['refscore'] = df['refscore'].astype(int)

        self.sentimentdf = df

        # print("sentiment df for reference:\n", self.sentimentdf.loc[:, :])


    # returns a dataframe with sentiment calculations
    def calculateSentiment(self, tweetdfs):

        sentimentScores = []

        #print(self.sentimentdfindexref)
        # iterate through dataframes
        for dataframe in tweetdfs:

            # iterate through all tweets in each dataframe
            for i, row in dataframe.iterrows():

                # iterate through all words in tweet
                for word in row[0].split():
                    #print("word:"+ word)

                    # retrieve index of row that contains the word
                    try:

                        rowname = (self.sentimentdf.index[self.sentimentdf['word'] == word].tolist())[0]
                        #print("row: ", rowname)

                        # increment instances in dataframe
                        #print("found word: ", word)
                        self.sentimentdf.loc[rowname, 'instances'] = int(self.sentimentdf.loc[rowname, 'instances'])+1

                    except IndexError:
                        pass

            #print("sentiment df before processing:\n", self.sentimentdf.loc[:, :])

            # calulate score column: score = refscore * instances
            self.sentimentdf['score'] = (self.sentimentdf['instances']*self.sentimentdf['refscore']).astype(int)

            #print("sentiment df after processing:\n", self.sentimentdf.loc[:, :],"\n")

            # calculate sentiment score: score / cumsum(instances)
            # print("cumsum score: ", self.sentimentdf['score'].cumsum(axis=0).iloc[-1])
            # print("cumsum instances: ", self.sentimentdf['instances'].cumsum(axis=0).iloc[-1])

            try:

                sentimentScore = float(self.sentimentdf['score'].cumsum(axis=0).iloc[-1]) / float(self.sentimentdf['instances'].cumsum(axis=0).iloc[-1])

            except ZeroDivisionError:

                # if no words are detected
                sentimentScore = 0

            sentimentScores.append(sentimentScore)

        return sentimentScores



# sc = sentimentCalculator()
#
# sc.loadSentimentData()
#
# #print(sc.sentimentdf.loc[:, :])