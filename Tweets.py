import csv
import re
from os import path
import datetime



class CreateDataSet:

    def __init__(self, csvFile):
        if path.exists(csvFile):
            self.csvInfo = self.getCsvData(csvFile)
            self.tweetsData = set() # set of dicks
            # self.tweetsData.add(dict(), {"username"})
            pass

    def getCsvData(self, csvFile):
        data = {}
        with open(csvFile, 'r') as csvfile:
            read = csv.DictReader(csvfile, delimiter=';')
            for i,entry in enumerate(read):
                data[i] = dict(entry)
                if (i > 500):
                    break
            # for i in range(len(data)):
            #     print(data[i]['timestamp'])
            #     print(data[i]['text'])
            #     print('\n')
            return data

    # '2020-12':
    #     "name": []
    #     "hashtag": []
    #     "page": []
    def getMostUsedHashtag(self):
        # r'#([^\s]*)[\s]'
        dicts = {"name", "hashtag"}
        for i in range(len(self.csvInfo)):
            time = self.csvInfo[i]["timestamp"] + "00"
            x = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S%z')
            timeString = str(x.year) + '-' + str('%02d' % x.month)
            name = re.finditer(r"@(\w[^\s]*)", str(self.csvInfo[i]["text"]));
            # for n in name:
            self.tweetsData.add(timeString)
            self.tweetsData[str(timeString)] = dicts
            # for i,entry in enumerate(self.tweetsData):


            # name = re.finditer(r"@(\w[^\s]*)", str(self.csvInfo[i]["text"]));
            # for h in name:
            #     print(h.group())
            # hashtag = re.finditer(r"#(\w[^\s]*)", str(self.csvInfo[i]["text"]))
            # website = re.finditer()
            # for h in hashtag:
            #     print(h.group())
        self.tweetsData = sorted(self.tweetsData)
        print(self.tweetsData)

    def getMostMentionedUserName(self):
        pass

    def getMostReferencedWebsite(self):
        pass
