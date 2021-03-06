import datetime
import os
import pymysql.cursors
import json

from flask import Flask
app = Flask(__name__)


class isrc_generator:

    with open('Init/config.json') as data_file:
        config_data = json.load(data_file)

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
                sql = "SELECT * FROM isrc_numbers WHERE name=%s"
                cursor.execute(sql, ("Membran"))
                result = cursor.fetchone()

                now = datetime.datetime.now()
                curYear = now.year % 100        #Retrieves two digit year format
                result['newNum'] = result['last_generated'] + amount    #Hypothetical new last_generated

                # Checks for year rollover, then increments code for how many are requested
                if result['last_gen_year'] < curYear:
                    result['last_gen_year'] = curYear
                    result['last_generated'] = amount

                #If newNum at or below upper limit, increment last_generated
                elif 0 <= result['newNum'] <= result['upper_limit']:
                    result['last_generated'] = result['last_generated']+amount
                #Otherwise must be beyond upper limit, do no change last_generated

                # Stores values that have now been used
                sql = "UPDATE isrc_numbers SET last_generated=%s AND last_gen_year=%s where name=%s"
                cursor.execute(sql, (result['last_generated'], result['last_gen_year'], "Membran"))

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

        if 0 <= codeDic['newNum'] <= codeDic['upper_limit']:
            codeDic['last_generated'] = codeDic['last_generated'] - amount + 1
            for x in range(0, amount):
                code = codeDic['country_code'] + codeDic['registrant_code'] + str(codeDic['last_gen_year']) + str(codeDic['last_generated']).zfill(5)
                codeDic['last_generated'] = codeDic['last_generated'] + 1
                codeCollection.append(code)
        else:
            code = 'ERROR: ISRC limit reached, contact administrator'
            codeCollection.append(code)

        return codeCollection

if __name__ == '__main__':
    b = isrc_generator()
    codes = b.generate(5)
    print(codes)
