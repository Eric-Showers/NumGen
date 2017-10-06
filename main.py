import os
from flask import Flask, request, send_from_directory
from BarcodeGen.Barcode_generator import Barcode_generator
from ISRCGen.isrc_generator import isrc_generator

app = Flask(__name__, static_url_path='')

@app.route('/')
def static_page():
    return send_from_directory('UI', 'NumGenUI.html')


@app.route('/barcode', methods=['POST'])
def createBarcode():
    productType = request.form['codeType']
    BCgen = Barcode_generator()
    codeDict = BCgen.getBarcodeNum(str(productType))
    return "Barcode: "+codeDict['code']+"<br>"+"Catalogue number: "+codeDict['strNum']

@app.route('/ISRC', methods=['POST'])
def createISRC():
    amount = int(request.form['amount'])
    ISRCgen = isrc_generator()
    codeList = ISRCgen.generate(amount)

    codeString = ""
    for lines in codeList:
        codeString = codeString + lines + "<br>"

    return codeString

def mainMethod():
    BCgenerator = Barcode_generator()
    code = BCgenerator.getBarcodeNum("233...")
    print(code)

if __name__ == '__main__':
    mainMethod()