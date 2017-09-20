import datetime
import os

class isrc_generator:

    country = 'DE'
    org = 'MEM'

    def generate(self, amount):
        now = datetime.datetime.now()
        curYear = now.year % 100        #Retrieves two digit year format

        #Accesses storage of previously assigned codes and finds last assigned code
        codeLibrary = open('ExistingCodes.txt', 'r+')
        for lines in codeLibrary:
            prevID = lines
        
        prevYear = int(prevID[5]+prevID[6])

        #Extracts last 5 digits of code and increments it's value by 1.
        newID = int(prevID[7:]) + 1

        if prevYear < curYear:
            newID = '00001'
        curYear = str(curYear)

        #Builds the code by concatenating country, org, year, and product codes
        code = ''
        
        for x in range(0,amount): 
            code = self.country + self.org + curYear + str(newID).zfill(5)
            codeLibrary.write('\n' + code)
            newID = newID + 1
        
        codeLibrary.close()

if __name__ == '__main__':
    b = isrc_generator()
    b.generate(5)