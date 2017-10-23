import json
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

    # Given a type, find an available ProdNum and call generator methods and return code
    def getBarcodeNum(self, prodNumName):

        newProd = self.get_prod_num(prodNumName)

        # Check that there was room for new product, otherwise skip gen. process
        if newProd['lastGen'] < newProd['limit']:
            # Create barcode without check digit
            newProd['strProdNum'] = str(newProd['prodNum'])
            if newProd['type'] == 'upca':
                newProd['code'] = str(newProd['firstDig']) + str(newProd['prodNum']%100000)
            elif newProd['type'] == 'ean13':
                newProd['code'] = str(newProd['firstDig']) + str(newProd['prodNum'])
            else:
                newProd['code'] = str(newProd['prodNum'])
            # Get check digit
            newProd['code'] = newProd['code'] + str(self.createCheckNum(newProd))
        else:
            newProd['code'] = "ERROR: product limit reached"
            newProd['strProdNum'] = "Contact administrator"
        return newProd

    def createCheckNum(self, newProd):
        codeStr = newProd['code']

        if newProd['type'] == 'upca':
            checkSum = 3*(int(codeStr[0])+int(codeStr[2])+int(codeStr[4])+int(codeStr[6])+int(codeStr[8])+int(codeStr[10]))+int(codeStr[1])+int(codeStr[3])+int(codeStr[5])+int(codeStr[7])+int(codeStr[9])
            check2 = checkSum%10
            if check2 != 0:
                check2 = 10 - check2
            return check2

        elif newProd['type'] == 'ean13':
            checkSum = int(codeStr[0])+int(codeStr[2])+int(codeStr[4])+int(codeStr[6])+int(codeStr[8])+int(codeStr[10]) + 3*(int(codeStr[1])+int(codeStr[3])+int(codeStr[5])+int(codeStr[7])+int(codeStr[9])+int(codeStr[11]))
            check2 = checkSum%10
            if check2 != 0:
                check2 = 10 - check2
            return check2

if __name__ == '__main__':
    temp = Barcode_generator()

    prodOne = temp.getBarcodeNum('233...')
    print(prodOne['code'])
    print(prodOne['strProdNum'])

    prodTwo = temp.getBarcodeNum('600...')
    print(prodTwo['code'])
    print(prodTwo['strProdNum'])