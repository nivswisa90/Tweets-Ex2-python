from Tweets import *


def main():
    tweet = CreateDataSet('tweets.csv')
    tweet.getMostUsedHashtag()


if __name__ == "__main__":
    main()
