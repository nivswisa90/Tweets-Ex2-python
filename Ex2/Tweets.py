import csv
import re
import numpy as np
from os import path
from pandas import Series as pd
# import pandas as pd
import datetime
import timeit
from urllib.parse import urlparse

class CreateDataSet:
    # Class Constructor
    def __init__(self, csvFile):
        if path.exists(csvFile):
            self.csvName = csvFile
            self.tweetsData = dict()
            self.processingData()            


    def processingData(self):
        # Function that reads a csv file and process the data into a dictonary order by month(YYYY-MM) with mentioned
        # username(@), hashtaghs(#) and website
        with open(self.csvName, 'r', encoding='utf-8') as csvfile:
            read = csv.DictReader(csvfile, delimiter=';')
            for line in read:
                #timeString is the month(YYYY-MM)
                timeString = line["timestamp"][:7]
                if timeString not in self.tweetsData:
                    self.tweetsData[timeString] = {"name": [], "hashtag": [], "web": []}
                text = line["text"]

                #Regex for hashtag
                hashtag = re.finditer(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))#([A-Za-z]+[A-Za-z0-9-_]+)', text)
                for h in hashtag:
                    hGroup = h.group()
                    if hGroup.lower() == '#bitcoin' or hGroup.lower() == '#bitcoins' or hGroup.lower() == '#btc':
                        break
                    else:
                        self.tweetsData[timeString]["hashtag"].append(hGroup)
                #Regex for mentioned username
                name = re.finditer(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9-_]+)', text)
                for n in name:
                    self.tweetsData[timeString]["name"].append(n.group())
                #Regex for website
                web = re.finditer(r'http(s)?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)
                for w in web:
                    hostname = urlparse(w.group().strip()).hostname
                    if hostname != None:
                        self.tweetsData[timeString]["web"].append(hostname)
                    else:
                        break

        self.tweetsData = self.getMode();


    def getMode(self):
        #Function that open a new csv file, insert the headers and order the required data by most referenced for each month
        outCsv = "tweet-data.csv"
        with open(outCsv, 'w', newline='', encoding='utf-8') as outCsvFile:
            csv_headers = ["Month", "Hashtag", "Name", "Web"]
            writer = csv.DictWriter(outCsvFile, csv_headers)
            writer.writeheader()
            #for every distinct month on the dictionary order the data by mode function and write it to the csv file
            for tweet in sorted(self.tweetsData):
                output = {}
                output["Month"] = tweet

                if self.tweetsData[tweet]["hashtag"]:
                    output["Hashtag"] = pd.mode(self.tweetsData[tweet]["hashtag"]).values[0]
                else:
                    output["Hashtag"] = "None"
                if self.tweetsData[tweet]["name"]:
                    output["Name"] = pd.mode(self.tweetsData[tweet]["name"]).values[0]
                else:
                    output["Name"] = "None"
                if self.tweetsData[tweet]["web"]:

                    output["Web"] = pd.mode(self.tweetsData[tweet]["web"]).values[0]
                else:
                    output["Web"] = "None"

                writer.writerow(output)