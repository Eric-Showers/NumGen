
class Barcode_generator:

    #Given the product number, generate ean13 barcode number
    def genEan13(self, prodNum):
        #TODO
        #Concatenate prodNum onto Membran ID, generate check number
        return prodNum

    #Given the product number, generate upca barcode number
    def genUpca(self, prodNum):
        num = '885150' + prodNum[0:5]

        check1 = (3*(int(num[0])+int(num[2])+int(num[4])+int(num[6])+int(num[8])+int(num[10])) 
                + int(num[1])+int(num[3])+int(num[5])+int(num[7])+int(num[9]))
        check2 = check1 % 10

        if check2 != 0:
            check2 = 10 - check2

        num = num + str(check2)
        return num

    #Given a type, find an available ProdNum and call generator methods and return code
    def getBarcodeNum(self, codeType):
        #TODO
        #Find an available product number

        prodNum = '123456'
        code = ''

        if codeType is 'ean13':
            code = self.genEan13(prodNum)
        elif codeType is 'upca':
            code = self.genUpca(prodNum)
        
        return code
    #Given a type, generate the number and image for a barcode
    def getBarcodeImg(self, codeType):
        #TODO
        #Call getBarcodeNum with type
        #Create image of barcode with number
        return getBarcodeNum(codeType)
        
if __name__ == '__main__':
    t = Barcode_generator()
    testNum = t.getBarcodeNum('upca')
    print(testNum)