import pandas as pd
import numpy as np
import sys

class sentiment:

    def __init__(self):

        # path to sentiment dictionary files
        # mac
        if sys.platform == "darwin":

            self.positiveWordsSrc = ["/Users/gabrielruoff/Dropbox/Stocks/StockOCAnalyzer/resources/opinion-lexicon-English/positive-words.txt"]
            self.negativeWordsSrc = ["/Users/gabrielruoff/Dropbox/Stocks/StockOCAnalyzer/resources/opinion-lexicon-English/negative-words.txt"]

        else:

            # windows
            self.positiveWordsSrc = ["C:/Users/GEruo/Dropbox/Stocks/stock_sentiment_analyzer/resources/opinion-lexicon-English/positive-words.txt",
                                     "C:/Users/GEruo/Dropbox/Stocks/stock_sentiment_analyzer/resources/subjclueslen-dict/positive.txt"]

            self.negativeWordsSrc = ["C:/Users/GEruo/Dropbox/Stocks/stock_sentiment_analyzer/resources/opinion-lexicon-English/negative-words.txt",
                                     "C:/Users/GEruo/Dropbox/Stocks/stock_sentiment_analyzer/resources/subjclueslen-dict/negative.txt"]

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

    def calculate_st_score(self, cells):

        print("scoring tweets...")

        # list of scores for each cell
        cell_scores = []

        # iterate through all tweets in each dataframe
        for cell in cells:
            # print("cell:", cell)

            for tweet in cell:

                # run tweet through scoring df
                # split into words
                for word in tweet.split():
                    #print("word:", word)

                    # retrieve index of row that contains the word
                    try:

                        rowname = (self.sentimentdf.index[self.sentimentdf['word'] == word].tolist())[0]
                        # print("row: ", rowname)

                        # increment instances in dataframe
                        #print("found word: ", word)
                        self.sentimentdf.loc[rowname, 'instances'] = int(self.sentimentdf.loc[rowname, 'instances']) + 1

                    except IndexError:
                        pass

            # score df for cell
            # calulate score column: score = refscore * instances
            self.sentimentdf['score'] = (self.sentimentdf['instances']*self.sentimentdf['refscore']).astype(int)

            try:

                st_score = float(self.sentimentdf['score'].cumsum(axis=0).iloc[-1]) / float(self.sentimentdf['instances'].cumsum(axis=0).iloc[-1])
                # print("st_score:", st_score)

            except ZeroDivisionError:

                # if no words are detected
                st_score = 0

            # clear scoring df
            self.reset_st_dataframe()

            # print("st_score 2:", st_score)
            cell_scores.append(st_score)

        #print(cell_scores)
        return cell_scores


    def reset_st_dataframe(self):

        # reset instances column
        self.sentimentdf['instances'] = np.array([0] * len(self.sentimentdf['instances']))

        # reset score column
        self.sentimentdf['score'] = np.array([0] * len(self.sentimentdf['score']))

# # TEST CODE
# st = sentiment()
#
# st.loadSentimentData()
#
# scores = st.calculate_st_score([['scaling in sizing up is good $ aapl $ amzn $ abbv $ bhc $ crm $ cmg $ tst $ ge $ f $ googl $ hlf $ iep $ ibm $ jnj $ ko $ msft $ nflx $ fb $ qsr $ tsla $ wfc $ jpm $ bac $ c $ cs $ btc $ googl $ msft $ ms $ gs $ jpm $ bac $', 'verified $2534 loss in $ msft long call option expiration 515', '$ msft new insider filing on microsoft corps director padmasree warrior', '$ twtr $ msft $ amzn $ qqq $ fb $ nflx $ xspa $ googl $ mrna $ penn $ nvda $ aapl futures $ bynd $ mark $ chk $ nkla calloptionstocks $ tmdi 15 minute candles i dont see a buying frenzy on this since the originalpictwittercomfli5u38w1y', 'not yet may very shortly in rough order of size $ amzn $ fb $ goog $ aapl $ nvda $ tsla $ skyy $ work $ estc $ msft $ v started in 2014 up 229 or so on a 6fig port $ wcld wasnt trading when i bought $ skyy otherwise i probably wouldve $ wcldd', 'fwsells $ msft walmsley emma n director of microsoft corp sold 49 shares on 20200608', 'june 9 plan esf $ spy $ spx $ nqf $ qqq $ iwm $ aapl $ nflx $ msft $ amzn $ googl $ fbpictwittercomv82pyv4v8r', 'ill be asking the sec soon whats going on with bankrupt hertz share price action $ aapl $ amzn $ abbv $ bhc $ crm $ cmg $ iep $ tst $ ge $ f $ googl $ hlf $ iep $ ibm $ jnj $ ko $ msft $ nflx $ fb $ qsr $ tsla $ wfc $ jpm $ bac $ c $ cs $ btc $ googl $ msft $ ms $ gs $ jpm $ bac $ c $ htz $$uber $ lyft $', 'thinkpad $ btc $ xrp $ spy $ spxl $ aapl $ msft $ v $ gs $ jnj $ ba $ trump', 'shannon referred you so you get a freestock claim your stock now without investing money first win a stock like netflix $ nflx apple $ aapl microsoft $ msft or facebook $ fb sign up and join robinhood using my']])
# print(scores)