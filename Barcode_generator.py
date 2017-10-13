import barcode  #viivakoodi
from barcode import generate
import pymysql.cursors
import json

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
                newProd['num'] = result['last_generated']+1
                newProd['type'] = result['barcode_type']
                newProd['firstDig'] = result['first_digits']
                sql = "UPDATE product_numbers SET last_generated=%s where name=%s"
                cursor.execute(sql,(newProd['num'], name))

            connection.commit()
        finally:
            connection.close()

        return newProd

    #Given a type, find an available ProdNum and call generator methods and return code
    def getBarcodeNum(self, prodNumName):

        newProd = {}
        newProd = self.get_prod_num(prodNumName)
        newProd['strNum'] = str(newProd['num'])
        if newProd['type'] == 'upca':
            newProd['code'] = str(newProd['firstDig']) + str(newProd['num']%100000)
        elif newProd['type'] == 'ean13':
            newProd['code'] = str(newProd['firstDig']) + str(newProd['num'])
        else:
            newProd['code'] = str(newProd['num'])

        codeObj = barcode.get(newProd['type'], str(newProd['code']))
        newProd['code'] = codeObj.get_fullcode()
        return newProd

    #Given a type, generate the number and image for a barcode
    def getBarcodeImg(self, prodNumName):

        newProd = self.getBarcodeNum(prodNumName)
        generate('%s'%(newProd['type']), u'%s'%(newProd['code']), output='%s_'%(newProd['type'])+'%s'%(newProd['code']))

        return 0

if __name__ == '__main__':
    t = Barcode_generator()
    testNum = t.getBarcodeNum('233...')
    print('upca: ' + testNum['code'])
    print('Catalogue number: ' + testNum['strNum'])
    testNum = t.getBarcodeNum('600...')
    print('ean13: ' + testNum['code'])
    print('Catalogue number: ' + testNum['strNum'])