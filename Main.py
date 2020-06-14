import sys
import datetime

if sys.version_info[0] < 3:
    import got
else:
    import got3 as got


def main():
    def printTweet(descr, t):
        print(descr)
        print("Username: %s" % t.username)
        print("Retweets: %d" % t.retweets)
        print("Text: %s" % t.text)
        print("Mentions: %s" % t.mentions)
        print("Hashtags: %s\n" % t.hashtags)

    # # Example 1 - Get tweets by username
    # tweetCriteria = got.manager.TweetCriteria().setUsername('barackobama').setMaxTweets(1)
    # tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
    #
    # printTweet("### Example 1 - Get tweets by username [barackobama]", tweet)

    # Example 2 - Get tweets by query search

    since = datetime.date(2020, 5, 30)
    since = str(since)

    print(type("2015-5-30"))
    print(type(since))

    tweetCriteria = got.manager.TweetCriteria()

    tweetCriteria.setQuerySearch('europe refugees')
    tweetCriteria.setSince(since)
    tweetCriteria.setUntil("2020-06-13")
    tweetCriteria.setMaxTweets(50)

    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    tw_list = [tweet.text for tweet in tweets]
    print(tw_list)


if __name__ == '__main__':
    main()
