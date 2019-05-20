from src import app,db
from src.models import User, Tests
from selenium import webdriver
import time
from flask import Flask, render_template, jsonify, request, redirect
import json
import platform
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from check import run_check
import os
from src.models import Token
from flask_cors import CORS
from flask import session
import uuid
from uuid import uuid4
from src import login_manager
from flask_login import current_user
import requests
import cloudinary.uploader
import cloudinary as Cloud
from dotenv import load_dotenv

load_dotenv()

Cloud.config.update = ({
    'cloud_name':os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.environ.get('CLOUDINARY_API_KEY'),
    'api_secret': os.environ.get('CLOUDINARY_API_SECRET')
})


@login_manager.request_loader
def load_user_from_request(request):
    print("I am trying to load the user from the headers.")
    # Login Using our Custom Header
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Token ', '', 1)
        token = Token.query.filter_by(uuid=api_key).first()
        if token:
            return token.user
    print("this is not working")
    return None


@app.route('/')
def index():
    return "this is it"

@app.route('/shopify-url', methods=['POST', 'GET'])
def shopify():
    data = request.get_json()
    print(data)
    print("current_user", current_user.id)
    product_url=data['product_url']
    cart=data['cartText']
    check=data['checkoutText']
    home=data['homepage']
    email=data['formEmail']
    first_name=data['firstName']
    second_name=data['secondName']
    address=data['address']
    city=data['city']
    post_code=data['post_code']
    run_check(product_url,cart,check,home,email,first_name,second_name,address,city,post_code)
    return jsonify({'data': data})

@app.route('/login', methods=['POST'])
def login():
    loginData= request.get_json('loginData')
    email= loginData['email']
    password= loginData['password']

    print(email, password)
    
    user= db.session.query(User).filter(User.email==email).first()  
 
    if user is not None and user.check_password(password):
        print("correct email and password")
        token_query= Token.query.filter_by(user_id=user.id)
        try:
            token = token_query.one()
        except NoResultFound:
            token = Token(user_id=user.id, uuid=str(uuid.uuid4().hex))    
            db.session.add(token)
            db.session.commit()           
        return jsonify({
            "loggedIn": True,
            "token": token.uuid,
            "user_id": token.user_id
        })
    else:
        print("wrong username or password")
        return jsonify({
            "error": "Something wrong with your login"
        })
    
    return jsonify({'loginData': loginData})

@app.route('/check', methods=['POST'])
def check():
    secret_token=request.headers.get('Authorization')
    print(secret_token)
    print(current_user.id)
    token= Token.query.filter_by(uuid=secret_token).first()
    if token:
        print(token.user_id)
        return jsonify({'user_id': token.user_id})
    
@app.route("/results", methods=['POST'])
def results():
    secret_token_results=request.headers.get('Authorization')
    print("results",current_user.id)
    #query database for Tests with User.id
    all_results=Tests.query.with_entities(Tests.id).filter_by(user_id=current_user.id).all()
    all_results_time= Tests.query.with_entities(Tests.time_created).filter_by(user_id=current_user.id).all()
    all_results_id= [r for (r,) in all_results]
    all_results_time_created= [i for (i,) in all_results_time]
    key_list=["id", "created_at"]
    results=[dict(zip(key_list, pair)) for pair in zip(all_results_id, all_results_time_created)]
    return jsonify(results)


@app.route("/results/<int:page_id>", methods= ['POST'])
def myid(page_id):
    secret_token_results=request.headers.get('Authorization')
    print("results",current_user.id)
    testing= db.session.query(Tests).filter(Tests.id==page_id).first()
    print(testing)
    print("aaaa",testing.id, testing.user_id, testing.product_page)
    # get screenshots from cloudinary
   
    type_payment_info= Cloud.CloudinaryImage(f"my_folder/{current_user.id}/type-payment-info{page_id}.png")
    click_checkout_button= Cloud.CloudinaryImage(f"my_folder/{current_user.id}/click-checkout-button{page_id}.png")
    personal_info_image= Cloud.CloudinaryImage(f"my_folder/{current_user.id}/person-information{page_id}.png")
    add_tocart_image= Cloud.CloudinaryImage(f"my_folder/{current_user.id}/add-to-cart{page_id}.png")
    click_payment_button_image= Cloud.CloudinaryImage(f"my_folder/{current_user.id}/clickpaymentbutton{page_id}.png")
    product_page_image= Cloud.CloudinaryImage(f"my_folder/{current_user.id}/product-page{page_id}.png")

    # print(testing_image_url)
    return jsonify({
        "id":testing.id,
        "product_page": testing.product_page,
        "add_to_cart": testing.add_to_cart,
        "go_to_checkout": testing.go_to_checkout,
        "payment_info": testing.payment_info,
        "payment_button": testing.payment_button,
        "personal_info": testing.personal_info,
        "personal_info_image": personal_info_image.url,
        "add_to_cart_image": add_tocart_image.url,
        "payment_page_image": click_payment_button_image.url,
        "product_page_image": product_page_image.url,
        "type_payment_image":  type_payment_info.url,
        "click_checkout_image": click_checkout_button.url
    })


if __name__ == '__main__':
    app.run()





