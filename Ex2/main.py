from Tweets import *


def main():
    CreateDataSet('tweets.csv')
    print(timeit.timeit())


if __name__ == "__main__":
    main()
