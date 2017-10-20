import json
import barcode  #viivakoodi
from barcode import generate
import pymysql.cursors

class Barcode_generator:

    with open('Init/config.json') as data_file:
        config_data = json.load(data_file)


    def get_prod_num(self, name):

        connection = pymysql.connect(host=self.config_data['Mysql']['host'],
                                     user=self.config_data['Mysql']['user'],
                                     password=self.config_data['Mysql']['password'],
                                     db=self.config_data['Mysql']['db'],
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM product_numbers WHERE name=%s"
                cursor.execute(sql, (name,))
                result = cursor.fetchone()

                # Update last_generated
                newProd = {}
                newProd['prodType'] = name
                newProd['lastGen'] = result['last_generated']
                newProd['type'] = result['barcode_type']
                newProd['firstDig'] = result['first_digits']
                newProd['limit'] = result['upper_limit']

                #Check for room for new code, if room then increment last_generated
                if newProd['lastGen'] < newProd['limit']:
                    newProd['prodNum'] = result['last_generated']+1
                #Otherwise no room so last_generated remains the same
                else:
                    newProd['prodNum'] = result['last_generated']

                sql = "UPDATE product_numbers SET last_generated=%s where name=%s"
                cursor.execute(sql, (newProd['prodNum'], name))

            connection.commit()
        finally:
            connection.close()

        return newProd

    #Given a type, find an available ProdNum and call generator methods and return code
    def getBarcodeNum(self, prodNumName):

        newProd = self.get_prod_num(prodNumName)

        #Check that there was room for new product, otherwise skip gen. process
        if newProd['lastGen'] < newProd['limit']:
            newProd['strProdNum'] = str(newProd['prodNum'])
            if newProd['type'] == 'upca':
                newProd['code'] = str(newProd['firstDig']) + str(newProd['prodNum']%100000)
            elif newProd['type'] == 'ean13':
                newProd['code'] = str(newProd['firstDig']) + str(newProd['prodNum'])
            else:
                newProd['code'] = str(newProd['prodNum'])

            codeObj = barcode.get(newProd['type'], str(newProd['code']))
            newProd['code'] = codeObj.get_fullcode()
        else:
            newProd['code'] = "ERROR: product limit reached"
            newProd['strProdNum'] = "Contact administrator"
        return newProd

    #Given a type, generate the number and image for a barcode
    def getBarcodeImg(self, prodNumName):

        newProd = self.getBarcodeNum(prodNumName)
        generate('%s'%(newProd['type']), u'%s'%(newProd['code']), output='%s_'%(newProd['type'])+'%s'%(newProd['code']))

        return 0

if __name__ == '__main__':
    temp = Barcode_generator()
    print(temp.getBarcodeNum('233...')['code'])
    print(temp.getBarcodeNum('600...')['code'])