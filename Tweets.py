import csv
import re
from os import path


class CreateDataSet:

    def __init__(self, csvFile):
        if path.exists(csvFile):
            self.csvInfo = self.getCsvData(csvFile)
        else:
            pass

    def getCsvData(self, csvFile):
        with open(csvFile, 'r') as csvfile:
            read = csv.DictReader(csvfile)
            for i,entry in enumerate(read):
                print(dict(entry))
                if (i > 9):
                    break
            return list(read)

    def getMostUsedHashtag(self):
        # r'#([^\s]*)[\s]'
        for i in range(len(self.csvInfo)):
            for line in self.csvInfo[i]:
                # print(self.csvInfo[i][line])
                hashtag = re.finditer(r"#(\w[^\s]*)", str(self.csvInfo[i][line]))
            for h in hashtag:
                print(h.group())

    def getMostMentionedUserName(self):
        pass

    def getMostReferencedWebsite(self):
        pass
