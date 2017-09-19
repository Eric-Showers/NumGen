import datetime
import os

class isrc_generator:

    def init(self):
        self.country = 'DE'
        self.org = 'MEM'

    def generate(self):
        now = datetime.datetime.now()
        curYear = now.year % 100        #Retrieves two digit year format
        curYear = str(curYear)

        codeLibrary = open('ExistingCodes.txt', 'r+')
        for lines in codeLibrary:
            #print(lines)
            prevID = lines
        #print('yeahboi')
        print(prevID)
        newID = int(prevID[7:]) + 1
        print(newID)
        newID = str(newID).zfill(5)

        code = ''
        code = code + self.country + self.org + curYear + newID
        print(code)
        codeLibrary.write('\n' + code)
        codeLibrary.close()

if __name__ == '__main__':
    b = isrc_generator()
    b.init()
    b.generate()