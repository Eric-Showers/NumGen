import os
from flask import Flask, request, send_from_directory, render_template
from BarcodeGen.Barcode_generator import Barcode_generator
from ISRCGen.isrc_generator import isrc_generator

app = Flask(__name__, static_url_path='')

@app.route('/', methods=['POST','GET'])
def static_page():
    #Default placeholder text
    returnBarcode = "Generated barcode will appear here"
    returnISRC = "Generated ISRC will apear here"

    #If called by post checks what is requested and updates return text variables
    if request.method == 'POST':
        if 'codeType' in request.form:
            returnBarcode = createBarcode(request.form['codeType'])
        elif 'amount' in request.form:
            returnISRC = createISRC(int(request.form['amount']))

    return render_template('index.html', returnBarcode=returnBarcode, returnISRC=returnISRC)

def createBarcode(productType):
    BCgen = Barcode_generator()
    codeDict = BCgen.getBarcodeNum(str(productType))
    return "Barcode: "+codeDict['code']+"\n"+"Catalogue number: "+codeDict['strNum']

def createISRC(amount):
    ISRCgen = isrc_generator()
    codeList = ISRCgen.generate(amount)

    codeString = ""
    for lines in codeList:
        codeString = codeString + lines + "\n"

    return codeString

def mainMethod():
    BCgenerator = Barcode_generator()
    code = BCgenerator.getBarcodeNum("233...")
    print(code)

if __name__ == '__main__':
    mainMethod()