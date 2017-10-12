import os
from flask import Flask, request, send_from_directory, render_template, url_for
from BarcodeGen.Barcode_generator import Barcode_generator
from ISRCGen.isrc_generator import isrc_generator

app = Flask(__name__, static_url_path='')

@app.route('/', methods=['POST','GET'])
def static_page():
    #Default placeholder text
    returnBarcode = "Generated barcode will appear here"
    returnISRC = ["Generated ISRC will apear here"]

    #If called by post checks what is requested and updates return text variables
    """if request.method == 'POST':
        if 'codeType' in request.form:
            returnBarcode = createBarcode(request.form['codeType'])
        elif 'amount' in request.form:
            returnISRC = createISRC(int(request.form['amount']))
    """
    return render_template('index.html', returnBarcode=returnBarcode, returnISRC=returnISRC)

@app.route('/barcode', methods=['POST'])
def createBarcode():
    BCgen = Barcode_generator()
    codeDict = BCgen.getBarcodeNum(request.form['codeType'])
    return codeDict['code']+"<br>"+codeDict['strNum']

@app.route('/ISRC', methods=['POST'])
def createISRC():
    ISRCgen = isrc_generator()
    codeList = ISRCgen.generate(int(request.form['amount']))
    codeString = ''

    for code in codeList:
        codeString = codeString + code + '<br>'

    return codeString

def mainMethod():
    BCgenerator = Barcode_generator()
    code = BCgenerator.getBarcodeNum("233...")
    print(code)

if __name__ == '__main__':
    mainMethod()
