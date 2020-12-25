# github desktop check
import csv
import re
from os import path
import datetime
from urllib.parse import urlparse

class CreateDataSet:

    def __init__(self, csvFile):
        if path.exists(csvFile):
            self.csvName = csvFile
            self.tweets = self.processingData()

    def getCsvData(self, csvFile):
        data = {}
        with open(csvFile, 'r') as csvfile:
            read = csv.DictReader(csvfile, delimiter=';')
            for i,entry in enumerate(read):
                data[i] = dict(entry)
                # if (i > 50000):
                #     break
            return data

    #def getMostUsedHashtag(self):
    def processingData(self):
        csvInfo = self.getCsvData(self.csvName)
        dicts = {"name": [], "hashtag": [], "web": []}
        tweetsData = dict()
        for i in range(len(csvInfo)):
            #Preparing the date('YYYY-MM')
            time = csvInfo[i]["timestamp"] + "00"
            x = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S%z')
            timeString = str(x.year) + '-' + str('%02d' % x.month)

            #Getting user names and hashtags
            name = re.finditer(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9-_]+)', csvInfo[i]["text"])
            hashtag = re.finditer(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))#([A-Za-z]+[A-Za-z0-9-_]+)', csvInfo[i]["text"])
            web = re.finditer(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',csvInfo[i]["text"] )
            for n in name:
                dicts["name"].append(n.group().strip())
            for h in hashtag:
                if h.group().lower() ==  '#bitcoin' or h.group().lower() ==  '#bitcoins' or h.group().lower() ==  '#btc':
                    res = re.findall('(#[^A-Z])', h.group())
                    if res != []:
                        dicts["hashtag"].append(h.group())
                    else:
                        break
                else:
                    dicts["hashtag"].append(h.group())
            for w in web:
                hostname = urlparse(w.group().strip()).hostname
                dicts["web"].append(hostname)
            tweetsData.update({timeString: dicts})

        # x = tweetsData.items()
        # sortedTweets = sorted(x)
        return tweetsData



    def getMostMentionedUserName(self):
        pass

    def getMostReferencedWebsite(self):
        pass
