import os
import json
from flask import Flask, request, send_from_directory, render_template, url_for
from Barcode_generator import Barcode_generator
from isrc_generator import isrc_generator

app = Flask(__name__, static_url_path='')

@app.route('/', methods=['POST','GET'])
def static_page():
    #Default placeholder text
    returnBarcode = "Generated barcode will appear here"
    returnISRC = ["Generated ISRC will apear here"]

    return render_template('index.html', returnBarcode=returnBarcode, returnISRC=returnISRC)

@app.route('/barcode', methods=['POST'])
def createBarcode():
    BCgen = Barcode_generator()
    codeDict = BCgen.getBarcodeNum(request.form['codeType'])

    json_data = json.dumps(codeDict)
    return json_data

@app.route('/ISRC', methods=['POST'])
def createISRC():
    ISRCgen = isrc_generator()
    codeList = ISRCgen.generate(int(request.form['amount']))

    json_data = json.dumps(codeList)
    return json_data

def mainMethod():
    BCgenerator = Barcode_generator()
    code = BCgenerator.getBarcodeNum("233...")
    print(code)

if __name__ == '__main__':
    mainMethod()
