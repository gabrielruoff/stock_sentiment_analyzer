import yfinance as yf
import itertools


class stockDataRetriever:

    def __init__(self):
        pass

    # retrieve stock data
    def retrieveData(self, tickers, period, interval):

        data = yf.download(  # or pdr.get_data_yahoo(...
            # tickers list or string as well
            tickers=tickers,

            # use "period" instead of start/end
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # (optional, default is '1mo')
            period=period,

            # fetch data by interval (including intraday if period < 60 days)
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            # (optional, default is '1d')
            interval=interval,

            # group by ticker (to access via data['SPY'])
            # (optional, default is 'column')
            group_by='ticker',

            # adjust all OHLC automatically
            # (optional, default is False)
            auto_adjust=True,

            # download pre/post regular market hours data
            # (optional, default is False)
            prepost=False,

            # use threads for mass downloading? (True/False/Integer)
            # (optional, default is True)
            threads=True,

        )

        return data

    def parseData(self, data, savedCols, multiindex=False):

        # get list of columns
        cols = list(data)

        # if dealing with a multiindexed df, we must get the multiindex column reference
        # slice savedcols so we can append while iterating
        if multiindex:

            for i, savedCol in enumerate(itertools.islice(savedCols, 0, 2)):

                for col in cols:

                    if col[1] == savedCol:
                        savedCols.append(col)

            # remove non-tupled data from list
            savedCols = savedCols[2:]

        # remove saved columns from list
        for col in savedCols:
            cols.remove(col)

        # remove remaining columns in list from dataframe
        data.drop(cols, axis=1, inplace=True)

    # split a multiindexed df into individual dfs characterized by parent index name
    def splitByMultiindex(self, data):

        returnedDfs = []

        # print("data list: ", list(data))

        for parentIndex in itertools.islice(list(data), 0, len(data), 2):
            returnedDfs.append(data.loc[:, [parentIndex[0]]])

        return returnedDfs

    # get % change from stock daily df
    def getDeltas(self, df):

        print(df.loc[:, :])

        deltas = []

        for i, row in enumerate(df.iterrows()):
            print("row:", row)

            deltas.append((df['Close'][i] - df['Open'][i]) / df['Open'][i])

        return list(reversed(deltas))

##### EXAMPLE CODE######

#s = stockDataRetriever()

#d = s.retrieveData("MSFT", "7d", "1d")
#s.parseData(d, ['Open', 'Close'])

#print(d)
