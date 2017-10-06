import barcode  #viivakoodi
from barcode import generate
import pymysql.cursors

class Barcode_generator:

    def get_prod_num(self, name):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='12345',
                                     db='learningDB',
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `*` FROM `product_numbers` WHERE `name`=%s"
                cursor.execute(sql, (name,))
                result = cursor.fetchone()

                # Update last_generated
                newProd = {}
                newProd['num'] = result['last_generated']+1
                newProd['type'] = result['barcode_type']
                sql = "UPDATE product_numbers SET last_generated=%d where name=\'%s\'"%(newProd['num'], name)
                cursor.execute(sql)

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
            newProd['code'] = '885150' + str(newProd['num']%100000)
        elif newProd['type'] == 'ean13':
            newProd['code'] = '405379' + str(newProd['num'])

        codeObj = barcode.get(newProd['type'], str(newProd['code']))
        newProd['code'] = codeObj.get_fullcode()
        return newProd

    #Given a type, generate the number and image for a barcode
    def getBarcodeImg(self, prodNumName):

        newProd = self.getBarcodeNum(prodNumName)
        generate('%s'%(codeType), u'%s'%(num), output='%s_'%(codeType)+'%s'%(num))

        return 0

if __name__ == '__main__':
    t = Barcode_generator()
    testNum = t.getBarcodeNum('233...')
    print('upca: ' + testNum['code'])
    print('Catalogue number: ' + testNum['strNum'])
    testNum = t.getBarcodeNum('600...')
    print('ean13: ' + testNum['code'])
    print('Catalogue number: ' + testNum['strNum'])
    #t.getBarcodeImg('ean13')
    #t.getBarcodeImg('upca')
