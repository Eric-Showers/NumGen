import datetime
import os

class isrc_generator:

    def init(self):
        self.country = 'DE'
        self.org = 'MEM'

    def generate(self):
        now = datetime.datetime.now()
        curYear = now.year % 100        #Retrieves two digit year format

        #Accesses storage of previously assigned codes and finds last assigned code
        codeLibrary = open('ExistingCodes.txt', 'r+')
        for lines in codeLibrary:
            prevID = lines
        
        prevYear = int(prevID[5]+prevID[6])

        #Extracts last 5 digits of code and increments it's value by 1.
        #Then casts as String and ensures that it is 5 characters, adding 0's as needed
        newID = int(prevID[7:]) + 1
        newID = str(newID).zfill(5)

        if prevYear < curYear:
            newID = '00001'
        curYear = str(curYear)

        #Builds the code by concatenating country, org, year, and product codes
        code = ''
        code = code + self.country + self.org + curYear + newID
        codeLibrary.write('\n' + code)
        codeLibrary.close()

if __name__ == '__main__':
    b = isrc_generator()
    b.init()
    b.generate()