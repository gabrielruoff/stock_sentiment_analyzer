from lib import got3 as got
import datetime
import re


class twitter:

    def __init__(self):

        # initialise sentiment calculator
        pass

    def get_cell_st_score(self, ticker, start_date, end_date, quantity, cell_size=datetime.timedelta(1)):
        # list of cell scores to return

        # list of cells- raw twitter data
        cells = []

        print(int((end_date - start_date).days))

        for start in (start_date + (n * cell_size) for n in range(int((end_date - start_date).days))):

            print("start:", start)

            since = str(start.date())
            print(since)

            until = start + cell_size
            until = str(until.date())
            print(until)

            tweetCriteria = got.manager.TweetCriteria()

            tweetCriteria.setQuerySearch(ticker)
            tweetCriteria.setSince(since)
            tweetCriteria.setUntil(until)
            tweetCriteria.setMaxTweets(quantity)

            tweets = got.manager.TweetManager.getTweets(tweetCriteria)

            # put tweets into list
            tw_list = [tweet.text for tweet in tweets]

            # clean up tweets in list
            for i in range(len(tw_list)):
                # remove links
                tw_list[i] = " ".join(re.sub("([^0-9A-Za-z$ \t])|(\w+:\/\/\S+)", "", tw_list[i]).split())

                # force lower case
                tw_list[i] = tw_list[i].lower()

            print(tw_list)

            # score list

            # add to cells
            cells.append(tw_list)

        # score list of cells
        cell_scores = 5

tw = twitter()

tw.get_cell_st_score("$MSFT", datetime.datetime(2020, 6, 7), datetime.datetime(2020, 6, 12, 0, 0), 10)
