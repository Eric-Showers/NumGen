import datetime
import os
import pymysql.cursors
import json

from flask import Flask
app = Flask(__name__)


class isrc_generator:

    with open('Init/config.json') as data_file:
        config_data = json.load(data_file)

    country = config_data['isrc']['country_code']
    org = config_data['isrc']['registrant_code']

    def get_next_num(self, amount):
        connection = pymysql.connect(host=self.config_data['Mysql']['host'],
                                     user=self.config_data['Mysql']['user'],
                                     password=self.config_data['Mysql']['password'],
                                     db=self.config_data['Mysql']['db'],
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Reads the last assinged code
                sql = "SELECT last_generated, last_gen_year FROM isrc_numbers WHERE country_code=%s AND registrant_code=%s"
                cursor.execute(sql,(self.country, self.org))
                result = cursor.fetchone()

                now = datetime.datetime.now()
                curYear = now.year % 100        #Retrieves two digit year format

                #Checks for upper limit on ISRC code (99999)
                if result['last_generated'] >= 99999:
                    result['last_generated'] = -1
                # Checks for year rollover, then increments code for how many are requested
                elif result['last_gen_year'] < curYear:
                    result['last_gen_year'] = curYear
                    result['last_generated'] = amount
                else:
                    # Update last_generated
                    result['last_generated'] = result['last_generated']+amount

                # Stores values that have now been used
                sql = "UPDATE isrc_numbers SET last_generated=%s where country_code=%s AND registrant_code=%s"
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
        
        if codeDic['last_generated'] >= 0:
            codeDic['last_generated'] = codeDic['last_generated'] - amount + 1
            for x in range(0, amount):
                code = self.country + self.org + str(codeDic['last_gen_year']) + str(codeDic['last_generated']).zfill(5)
                codeDic['last_generated'] = codeDic['last_generated'] + 1
                codeCollection.append(code)
        else:
            code = 'ERROR: ISRC limit reached, contact Administrator'
            codeCollection.append(code)
            
        return codeCollection

if __name__ == '__main__':
    b = isrc_generator()
    codes = b.generate(5)
    print(codes)
