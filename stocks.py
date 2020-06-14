import yfinance as yf
from datetime import datetime
import time
import numpy as np

class stockDataHandler:

    def __init__(self):
        pass

    # retrieve stock data from yfinance api
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
            #group_by='ticker',

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

    def handleStockData(self, tickers, start_date, end_date=datetime.now(), cell_size="1d"):

        stockData = []

        # calculate period of days
        period = np.busday_count(start_date.date(), end_date.date())
        period = str(period) + 'd'
        print("period:", period)

        # list of stock cell dataframes across target period

        for ticker in tickers:

            # retrieve dataframe (ticker[1:] removes '$' from ticker)
            ticker_df = self.retrieveData(ticker[1:], period, cell_size)

            # print(ticker_df.loc[:, :])

            # get delta from dataframe and add to list
            ticker_deltas = ((ticker_df['Close']-ticker_df['Open'])/ticker_df['Open']).tolist()

            # add list of ticker deltas to stockData list
            stockData.append(ticker_deltas)

        # return list of ticker data which itself is a list of deltas
        return stockData


# # Testing
#
# t0 = time.time()
# sdh = stockDataHandler()
#
# tickers = ['$MSFT', '$AAPL']
# start_date = datetime(2020, 6, 3, 0, 0, 0)
#
# # print(sdh.retrieveData(tickers, '10', '1d' ))
#
# stockData  = sdh.handleStockData(tickers, start_date)
# print("took:", time.time()-t0, "seconds")
# print(stockData)
# print(len(stockData[0]))
