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
                sql = "SELECT last_generated, year FROM isrc WHERE country=%s AND org=%s"
                cursor.execute(sql,(self.country, self.org))
                result = cursor.fetchone()

                now = datetime.datetime.now()
                curYear = now.year % 100        #Retrieves two digit year format

                # Checks for year rollover, then increments code for how many are requested
                if result['last_gen_year'] < curYear:
                    result['last_gen_year'] = curYear
                    result['last_generated'] = amount
                else:
                    # Update last_generated
                    result['last_generated'] = result['last_generated']+amount

                # Stores values that have now been used
                sql = "UPDATE isrc SET last_generated=%s where country=%s AND org=%s"
                cursor.execute(sql,(result['last_generated'], self.country, self.org))

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
        codeDic['last_generated'] = codeDic['last_generated'] - amount + 1
        for x in range(0, amount):
            code = codeDic['country_code'] + codeDic['registrant_code'] + str(codeDic['last_gen_year']) + str(codeDic['last_generated']).zfill(5)
            codeDic['last_generated'] = codeDic['last_generated'] + 1
            codeCollection.append(code)

        return codeCollection

if __name__ == '__main__':
    b = isrc_generator()
    codes = b.generate(5)
    print(codes)
