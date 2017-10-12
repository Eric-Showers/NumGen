import datetime
import os
import pymysql.cursors

from flask import Flask
app = Flask(__name__)


class isrc_generator:

    country = 'DE'
    org = 'MEM'

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
                sql = "SELECT last_gen, year FROM isrc WHERE country=%s AND org=%s"
                cursor.execute(sql,(self.country, self.org))
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
                sql = "UPDATE isrc SET last_gen=%s where country=%s AND org=%s"
                cursor.execute(sql,(result['last_gen'], self.country, self.org))

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
        codeDic['las_gen'] = codeDic['last_gen'] - amount + 1
        for x in range(0, amount):
            code = self.country + self.org + str(codeDic['year']) + str(codeDic['last_gen']).zfill(5)
            codeDic['last_gen'] = codeDic['last_gen'] + 1
            codeCollection.append(code)

        return codeCollection

if __name__ == '__main__':
    b = isrc_generator()
    codes = b.generate(5)
    print(codes)
