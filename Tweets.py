import csv
import re
import numpy as np
from os import path
import pandas as pd
import datetime
from urllib.parse import urlparse

class CreateDataSet:

    def __init__(self, csvFile):
        if path.exists(csvFile):
            self.csvName = csvFile
            self.tweetsData = dict()
            self.processingData()            

            # getMode(self)

    # def getCsvData(self, csvFile):
    #     data = {}
    #     with open(csvFile, 'r') as csvfile:
    #         read = csv.DictReader(csvfile, delimiter=';')
    #         for i,entry in enumerate(read):
    #             data[i] = dict(entry)
    #             if (i > 500):
    #                 break
    #         return data

    #def getMostUsedHashtag(self):
    
    def processingData(self):
        with open(self.csvName, 'r', encoding='utf-8') as csvfile:
            read = csv.DictReader(csvfile, delimiter=';', quotechar='"')
            # i = 0
            for line in read:
                # i += 1
                time = line["timestamp"] + "00"
                x = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S%z')
                timeString = str(x.year) + '-' + str('%02d' % x.month)
                if timeString not in self.tweetsData:
                    self.tweetsData[timeString] = {"name": [], "hashtag": [], "web": []}
                text = line["text"]

                hashtag = re.finditer(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))#([A-Za-z]+[A-Za-z0-9-_]+)', text)
                for h in hashtag:
                    hGroup = h.group()
                    if hGroup.islower() == False:
                        if hGroup.lower() ==  '#bitcoin' or hGroup.lower() ==  '#bitcoins' or hGroup.lower() ==  '#btc':
                            res = re.findall('(#[^A-Z])', hGroup)
                            if res != []:
                                self.tweetsData[timeString]["hashtag"].append(hGroup)
                            else:
                                break
                        else:
                            self.tweetsData[timeString]["hashtag"].append(hGroup)
                    else:
                        self.tweetsData[timeString]["hashtag"].append(hGroup)

                name = re.finditer(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9-_]+)', text)
                for n in name:
                    self.tweetsData[timeString]["name"].append(n.group())

                # web = re.finditer(r'http(s)?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)
                web = re.finditer(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))",text)
                for w in web:
                    hostname = urlparse(w.group().strip()).hostname
                    if hostname != None:
                        self.tweetsData[timeString]["web"].append(hostname)


                # if i > 50000:
                #     break

        self.tweetsData = self.getMode();


    def getMode(self):
        outCsv = "tweet-data.csv"
        with open(outCsv, 'w', newline='', encoding='utf-8') as outCsvFile:
            csv_headers = ["Month", "Hashtag", "Name", "Web"]
            writer = csv.DictWriter(outCsvFile, csv_headers)
            writer.writeheader()

            for tweet in sorted(self.tweetsData):
                output = {}
                output["Month"] = tweet

                if self.tweetsData[tweet]["hashtag"]:
                    output["Hashtag"] = sorted(pd.Series.mode(self.tweetsData[tweet]["hashtag"])).values[0]
                else:
                    output["Hashtag"] = "None"
                if self.tweetsData[tweet]["name"]:
                    output["Name"] = sorted(pd.Series.mode(self.tweetsData[tweet]["name"])).values[0]
                else:
                    output["Name"] = "None"
                if self.tweetsData[tweet]["web"]:

                    output["Web"] = sorted(pd.Series.mode(self.tweetsData[tweet]["web"])).values[0]
                else:
                    output["Web"] = "None"

                writer.writerow(output)