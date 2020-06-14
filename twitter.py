from lib import got3 as got
import datetime
import re
import sentiment


class tweethandler:

    def __init__(self):

        # initialise sentiment calculator
        self.st = sentiment.sentiment()
        self.st.loadSentimentData()

    def get_cell_st_scores(self, ticker, start_date, end_date, quantity, cell_size=datetime.timedelta(1)):
        # list of cell scores to return
        cell_scores = []

        # list of cells- raw twitter data
        cells = []

        for start in (start_date + (n * cell_size) for n in range(int((end_date - start_date).days))):

            print("🐦-> ", end="")

            since = str(start.date())

            until = start + cell_size
            until = str(until.date())

            #print("since:", since, "until:", until)

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

            # add to cells
            # if tweet is from a Saturday or Sunday
            # print((start).strftime("%A"))
            if (start).strftime("%A") == "Sunday" or (start).strftime("%A") == "Saturday":

                for element in tw_list:

                    cells[-1].append(element)

            else:

                cells.append(tw_list)

        print("")

        # score list of cells
        cell_scores = self.st.calculate_st_score(cells)

        return cell_scores

# TEST CODE
# tw = tweethandler()
#
# scores = tw.get_cell_st_scores("$MSFT", datetime.datetime(2020, 6, 3), datetime.datetime(2020, 6, 13, 0, 0), 10)
#
# print(len(scores))
# print(scores)
