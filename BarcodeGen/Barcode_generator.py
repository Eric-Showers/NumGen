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
                sql = "SELECT `last_generated` FROM `product_numbers` WHERE `name`=%s"
                cursor.execute(sql, (name,))
                result = cursor.fetchone()
                #print(result['last_generated'])

                # Update last_generated
                newNum = result['last_generated']+1
                #print(newNum)
                sql = "UPDATE product_numbers SET last_generated=%d where name=\'%s\'"%(newNum, name)
                #print(sql)
                cursor.execute(sql)

            connection.commit()
        finally:
            connection.close()

        return str(result['last_generated'])

    #Given a type, find an available ProdNum and call generator methods and return code
    def getBarcodeNum(self, codeType, prodNumName):
        #TODO
        #Find an available product number

        prodNum = self.get_prod_num(prodNumName)
        if codeType is 'upca':
            num = '885150' + prodNum[1:]
        elif codeType is 'ean13':
            num = '405379' + prodNum

        codeObj = barcode.get(codeType, num)
        code = codeObj.get_fullcode()
        return code

    #Given a type, generate the number and image for a barcode
    def getBarcodeImg(self, codeType):

        num = self.getBarcodeNum(codeType)
        generate('%s'%(codeType), u'%s'%(num), output='%s_'%(codeType)+'%s'%(num))

        return 0

if __name__ == '__main__':
    t = Barcode_generator()
    testNum = t.getBarcodeNum('upca','233')
    print('upca: ' + testNum)
    testNum = t.getBarcodeNum('ean13','600')
    print('ean13: ' + testNum)
    #t.getBarcodeImg('ean13')
    #t.getBarcodeImg('upca')
