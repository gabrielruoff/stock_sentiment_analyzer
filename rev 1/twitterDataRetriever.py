import tweepy as tw
import pandas as pd
import os
import io
import re
import datetime
import time

class twitterDataRetriever:

    def __init__(self):

        self.consumer_key = 'jgou2mwBcYlsoMAVWS6AxMuz9'
        self.consumer_secret = 'nsnkswvaK34SSM6ak4n8RPvvtqjtyp5VrzvPeZgF3oByq05xjN'
        self.access_token = '705040220547321856-pPTLCKPeKkt9nrXpmz7rACRKVprw0HK'
        self.access_token_secret = 'FN7wmynHZoNAeviLSz5qPRevOtjNvH41fpud0tTxEY3MO'

        # define api instance
        auth = tw.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tw.API(auth, wait_on_rate_limit=True)

        # pandas options
        pd.set_option('display.max_rows', 100000)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 500)
        pd.set_option('display.max_colwidth', None)

    # returns list of strings containing tweets with certain terms
    def retrieveByTerm(self, terms, since, until, quantity, ignoreRetweets=True):

        # define variables
        returnedData = []
        cursors = []

        if ignoreRetweets:

            for i, term in enumerate(terms):
                terms[i] = term + " Filter:retweets"

        # get cursor objects with tweets
        for term in terms:

            cursors.append(tw.Cursor(self.api.search, q=term, lang="en", since=since, until=until, tweet_mode='extended', count=quantity, wait_on_rate_limit=True).items(quantity))

        # iterate through each cursor
        for cursor in cursors:

            tweets = []
            timestamps = []

            # extract tweet data into temporary arrays
            for tweet in cursor:
                tweets.append(tweet.full_text)
                timestamps.append(tweet.created_at)

            # create dataframe from temporary arrays
            tweetdf = pd.DataFrame(tweets, index=timestamps, columns=['text'])

            # remove tweets with duplicate timestamps
            tweetdf = tweetdf.loc[~tweetdf.index.duplicated(keep='first')]

            # add dataframe to returned data
            returnedData.append(tweetdf)

        # return array of dataframes
        return returnedData


    # cleans up tweet data in list of tweets
    def cleanupTweetData(self, tweets, forceLowerCase=True, removeurls=True, disQSpammedTags=True, spammedTagsLim=5):

        # force lower case
        if forceLowerCase:

            for dataframe in tweets:

                for i, row in dataframe.iterrows():

                    # replace text with lowercase
                    dataframe.loc[i, "text"] = [dataframe.loc[i, "text"].lower() for word in row][0]

        # remove URLs
        if removeurls:

            for dataframe in tweets:

                for i, row in dataframe.iterrows():
                    dataframe.loc[i, "text"] = " ".join(re.sub("([^0-9A-Za-z$ \t])|(\w+:\/\/\S+)", "", dataframe.loc[i, "text"]).split())

        # disqualifies spammed tage i.e. $MSFT $F $AAPL $AMD $GE....
        if disQSpammedTags:

            for dataframe in tweets:

                for i, row in dataframe.iterrows():

                    # if spammed tags are detected
                    if dataframe.loc[i, "text"].count('$') > spammedTagsLim:

                        # drop row
                        dataframe.drop(row.name, axis=0, inplace=True)

    # retrieve dataframes for a list of terms over a range of dates with a specified quantity, cell size, and step
    def retrieveRangeByTerm(self, terms, start_date, end_date, date_step, quantity, ignoreRetweents=True):

        start_dt = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        twRangeData = []

        # find differene between end and start dates
        datedif = int((end_dt - start_dt).days)

        print("fetching tweet-date range data")

        for start in (start_dt + (n*date_step) for n in range(datedif)):

            f = io.open("out.txt", 'w', encoding="utf-8")

            #print(("getting day: ", start_date, end_date), file=f)
            end = start+date_step

            end = str(end.date())

            # retrieve tweet data for each cell in range and add to an array of tuples
            tweets = self.retrieveByTerm(terms, start_date, end, quantity, ignoreRetweets=ignoreRetweents)
            twRangeData.append(tweets)#, [start_dt, end_dt]))

            for tweetdf in tweets:

                print("\nreturned tweet df:\n", file=f)
                print(tweetdf.loc[:, :], file=f)
                print("\n\n", file=f)

            # break between api requests
            time.sleep(1)
            print("🐦 -> ", end='')

            # close the log file
            f.close()

        print('')

        f = io.open("out.txt", 'w', encoding="utf-8")
        print("twRangeData:", file=f)
        print(twRangeData, file=f)
        f.close()

        return twRangeData

    # get 'x' column to be used in ML algorithm. returns [ [sentiment score day 1, 2, 3..] for each ticker ]
    # def rangeToMLX(self, twRangeData, tickers):



#### TESTING

# tdr = twitterDataRetriever()
#
# terms = ["$MSFT", "$AAPL"]
#
# returnedTweets = tdr.retrieveByTerm(terms.copy(), "2019-11-16", 1)
# print(type(returnedTweets[0]))
# print("Tweets before cleanup:")
# print("MSFT Tweets: ", returnedTweets[terms.index("$MSFT")],"\n\nAAPL Tweets: ", returnedTweets[terms.index("$AAPL")])
#
# from pandas import ExcelWriter
#
# writer = ExcelWriter('PythonExportPre.xlsx')
# returnedTweets[0].to_excel(writer,'Sheet5')
# writer.save()
#
# # parse tweets
# print("\n\nTweets after cleanup: ")
# tdr.cleanupTweetData(returnedTweets, disQSpammedTags=5)
#
# print("MSFT Tweets: ", returnedTweets[terms.index("$MSFT")],"\n\nAAPL Tweets: ", returnedTweets[terms.index("$AAPL")])
#
# writer = ExcelWriter('PythonExportPost.xlsx')
# returnedTweets[0].to_excel(writer,'Sheet5')
# writer.save()