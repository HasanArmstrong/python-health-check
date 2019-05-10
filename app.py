from selenium import webdriver
import time
from flask import Flask, render_template, jsonify, request
import json
from flask_cors import CORS
import platform
from check import run_check

app= Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shopify-url', methods=['POST', 'GET'])
def shopify():
    data = request.get_json()
    product_url=data['product_url']
    # collection_url=data['collection_url']
    run_check(product_url)
    # run_check(collection_url)
    return jsonify({'data': data})

    
@app.route('/check')
def check():
    pass
    

if __name__ == '__main__':
    app.run()






