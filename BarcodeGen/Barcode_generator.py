import barcode  #viivakoodi
from barcode import generate

class Barcode_generator:
    #Given a type, find an available ProdNum and call generator methods and return code
    def getBarcodeNum(self, codeType):
        #TODO
        #Find an available product number

        prodNum = '123456'
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

        return self.getBarcodeNum(codeType)
        
if __name__ == '__main__':
    t = Barcode_generator()
    testNum = t.getBarcodeNum('upca')
    print('upca: ' + testNum)
    testNum = t.getBarcodeNum('ean13')
    print('ean13: ' + testNum)
    t.getBarcodeImg('ean13')
    t.getBarcodeImg('upca')