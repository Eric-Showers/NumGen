import datetime
import os
import pymysql.cursors

from flask import Flask
app = Flask(__name__)


class isrc_generator:

    country = 'DE'
    org = 'MEM'

    @app.route('/generate')
    def hello_world():
        codes = []
        temp = isrc_generator()
        codes = temp.generate(5)
        retLine = ''
        for lines in codes:
            retLine = retLine + '\n' + lines

        return retLine

    def get_next_num(self, amount):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='12345',
                                     db='learningDB',
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Reads the last assinged code
                sql = "SELECT `last_gen`, `year` FROM isrc WHERE country=\'%s\' AND org=\'%s\'"%(self.country, self.org)
                cursor.execute(sql)
                result = cursor.fetchone()

                now = datetime.datetime.now()
                curYear = now.year % 100        #Retrieves two digit year format

                # Checks for year rollover, then increments code for how many are requested
                if result['year'] < curYear:
                    result['year'] = curYear
                    result['last_gen'] = amount
                else:
                    # Update last_gen
                    result['last_gen'] = result['last_gen']+amount

                # Stores values that have now been used
                sql = "UPDATE isrc SET last_gen=%d where country=\'%s\' AND org=\'%s\'"%(result['last_gen'], self.country, self.org)
                cursor.execute(sql)

            connection.commit()
        finally:
            connection.close()

        return result

    def generate(self, amount):

        #Accesses storage of previously assigned codes and finds last assigned (year & code)
        codeDic = self.get_next_num(amount)

        #Builds the code by concatenating country, org, year, and product codes
        code = ''
        codeCollection = []
        for x in range(0, amount):
            code = self.country + self.org + str(codeDic['year']) + str(codeDic['last_gen']).zfill(5)
            codeDic['last_gen'] = codeDic['last_gen'] - 1
            codeCollection.append(code)

        return codeCollection

if __name__ == '__main__':
    b = isrc_generator()
    codes = b.generate(5)
    print(codes)
    b.hello_world()
