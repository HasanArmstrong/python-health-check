
# This will work using headless Chrome for any Desktop OS (Windows, MacOS, Linux Desktop)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import platform
import time
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement
from src.models import Tests
from src.models import User
from src import db
from flask_login import current_user
from flask import session, Flask
from sqlalchemy import desc
import cloudinary.uploader
import cloudinary as Cloud

def run_check(url,cart_text,checkout_text,home_url,placeholder_email,first_name,last_name,address,city,post_code):
    print(cart_text)
    # Gets the path to the right chromedriver
    path = "$PATH:/Users/pc/Desktop/shophealthcheck" + platform.system()
    links = [url]
    options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    # must install linux browser `sudo apt-get install -y chromium-browser` in Linux
    if(platform.system() == 'Linux'):
        options.binary_location = '/usr/bin/chromium-browser'
    options.add_argument("disable-infobars")  # disabling infobars
    options.add_argument("--disable-extensions")  # disabling extensions
    options.add_argument("--disable-gpu")  # applicable to windows os only
    # overcome limited resource problems
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")  # Bypass OS security model
    # Thanks to https://stackoverflow.com/a/50642913/2291648 for explaining the arguments above

    with webdriver.Chrome("chromedriver", chrome_options=options) as driver:
        # these values represent the sizes of the entire browser window and not the viewport.
        for link in links:
            desktop = {'output': str(link) + '-desktop.png',
                    'width': 2200,
                    'height': 1800}
            tablet = {'output': str(link) + '-tablet.png',
                    'width': 1200,
                    'height': 1400}
            mobile = {'output': str(link) + '-mobile.png',
                    'width': 680,
                    'height': 1200}
            linkWithProtocol = 'https://' + str(link)

            # set the window size for desktop
            #product page 
        # driver.set_window_size(desktop['width'], desktop['height'])
        # driver.get(linkWithProtocol)
        # driver.save_screenshot("product_page.png")

        def payment(go_product_page,go_add_to_cart,go_checkout_text,go_personal_info):
        #go to payment page and enter information
            try:
                print(go_product_page,go_add_to_cart,go_checkout_text,go_personal_info)
                print(checkout_text)
                time.sleep(4)
                # drive.save_screenshot("shippinginfo.png")
                # time.sleep(4)
                driver.find_element_by_id("continue_button").click()
                print("click continue to checkout button")
                time.sleep(7)

                driver.switch_to.frame(1)
                time.sleep(2)
                driver.find_element_by_id("number").send_keys("6242976511234489")
                driver.switch_to_default_content()
                time.sleep(2)

                driver.switch_to.frame(2)
                driver.find_element_by_id("name").send_keys("Chares Lee")
                time.sleep(2)
                driver.switch_to_default_content()

                driver.switch_to.frame(3)
                expiry= driver.find_element_by_id("expiry")
                expiry.send_keys("0927")
                driver.switch_to_default_content()
                time.sleep(1)

                driver.switch_to.frame(4)
                security_code= driver.find_element_by_id("verification_value")
                security_code.send_keys("101")
                driver.switch_to_default_content()
                time.sleep(1)
                driver.save_screenshot("type-payment-info.png")
                go_payment_info= True
                driver.switch_to_default_content()
                driver.find_element_by_id("continue_button").click()
                driver.save_screenshot("clickpaymentbutton.png")
                print("click pay now button")
                go_payment_button= True
                time.sleep(5)
                print("--------", current_user.id)
                db.session.add(Tests(user_id=current_user.id, product_page=go_product_page, add_to_cart=go_add_to_cart,go_to_checkout=go_checkout_text,personal_info=go_personal_info, payment_info=go_payment_info, payment_button=go_payment_button))
                db.session.commit()
                print("submmited to database")
                #submit to cloduinary
                last_test= Tests.query.order_by(desc('id')).first()
                page_id= last_test.id

                Cloud.uploader.upload("./type-payment-info.png", 
                folder = f"my_folder/{current_user.id}/", 
                public_id = f"type-payment-info{page_id}")

                Cloud.uploader.upload("./add-to-cart.png", 
                folder = f"my_folder/{current_user.id}/", 
                public_id = f"add-to-cart{page_id}")

                Cloud.uploader.upload("./click-checkout-button.png", 
                folder = f"my_folder/{current_user.id}/", 
                public_id = f"click-checkout-button{page_id}")

                Cloud.uploader.upload("./clickpaymentbutton.png", 
                folder = f"my_folder/{current_user.id}/", 
                public_id = f"clickpaymentbutton{page_id}")

                Cloud.uploader.upload("./product-page.png", 
                folder = f"my_folder/{current_user.id}/", 
                public_id = f"product-page{page_id}")

                Cloud.uploader.upload("./person-information.png", 
                folder = f"my_folder/{current_user.id}/", 
                public_id = f"person-information{page_id}")

                print("Submitted to Cloudinary")
                print(Tests.query.all())

                time.sleep(20)
                type_payment_info= Cloud.CloudinaryImage(f"my_folder/{current_user.id}/type-payment-info{page_id}.png")
                click_checkout_button= Cloud.CloudinaryImage(f"my_folder/{current_user.id}/click-checkout-button{page_id}.png")
                personal_info_image= Cloud.CloudinaryImage(f"my_folder/{current_user.id}/person-information{page_id}.png")
                add_tocart_image= Cloud.CloudinaryImage(f"my_folder/{current_user.id}/add-to-cart{page_id}.png")
                click_payment_button_image= Cloud.CloudinaryImage(f"my_folder/{current_user.id}/clickpaymentbutton{page_id}.png")
                product_page_image= Cloud.CloudinaryImage(f"my_folder/{current_user.id}/product-page{page_id}.png")

                print(type_payment_info.url)
                print(click_checkout_button.url)
                print(personal_info_image.url)
                print(add_tocart_image.url)
                print(click_payment_button_image.url)
                print(product_page_image.url)
                product_page_email= None

                product_page_email=''
                add_to_cart_email=''
                personal_info_email=''
                checkout_text_email=''
                payment_info_email=''
                payment_button_email=''

                if go_product_page:
                    product_page_email= "Pass"
                else: 
                    product_page_email= "Fail"
          
                if go_add_to_cart:
                    add_to_cart_email= "Pass"
                else:
                    add_to_cart_email= "Fail"

                if go_personal_info:
                    personal_info_email= "Pass"
                else: 
                    personal_info_email= "Fail"

                if go_checkout_text:
                    checkout_text_email= "Pass"
                else:
                    checkout_text_email= "Fail"

                if go_payment_info:
                    payment_info_email= "Pass"
                else: 
                    payment_info_email= "Fail"

                if go_payment_button:
                    payment_button_email= "Pass"
                else: 
                    payment_button_email= "Fail"

                requests.post("https://api.mailgun.net/v3/sandbox46bbbb850d304e6396c09ddbb7703a21.mailgun.org/messages",
                auth=("api", "1ea281e23190f090dcfe8d12336cad0c-7bce17e5-9bac263c"),
                data={"from": "Hasan: <postmaster@sandbox46bbbb850d304e6396c09ddbb7703a21.mailgun.org>",
                "to": "phananhtuan1011@gmail.com",
                "subject": "Health Check Results: ",
                "text": f"This is working",
                "html": f"<html><h1 style='text-align:center'>Health Check Report</h1></br><h3 style='text-align:center'>Product Page</h3><h3>Test Result:{product_page_email}</h3><img src={product_page_image.url} width='1000' height='500'><h3 style='text-align:center'>Click Add to Cart Button<h3><h3>Test Result:{add_to_cart_email}</h3><img src={add_tocart_image.url} width='1000' height='500'/><h3 style='text-align:center'>Type Shipping Info<h3><h3>Test Result:{personal_info_email}</h3><img src={personal_info_image.url} width='1000' height='500'/><h3 style='text-align:center'>Click Checkout Button<h3><h3>Test Result:{checkout_text_email}</h3><img src={click_checkout_button.url} width='1000' height='500'/><h3 style='text-align:center'>Type payment information<h3><h3>Test Result:{payment_info_email}</h3><img src={type_payment_info.url} width='1000' height='500'/><h3 style='text-align:center'>Click Payment button<h3><h3>Test Result:{payment_button_email}</h3><img src={click_payment_button_image.url} width='1000' height='500'/><html/>"})
                print("send email")

            except:
                go_payment_info= False
                go_payment_button= False
                db.session.add(Tests(user_id=current_user.id, product_page=go_product_page, add_to_cart=go_add_to_cart,go_to_checkout=go_checkout_text,personal_info=go_personal_info, payment_info=go_payment_info, payment_button=go_payment_button))
                db.session.commit()
                print("submmited to database")
                print("--------", current_user.id)
                print(Tests.query.all())
                print("payment form input didn't work but submitted to database")
                last_test= Tests.query.order_by(desc('id')).first()
                page_id= last_test.id

                Cloud.uploader.upload("./type-payment-info.png", 
                folder = f"my_folder/{current_user.id}/", 
                public_id = f"type-payment-info{page_id}")

                Cloud.uploader.upload("./add-to-cart.png", 
                folder = f"my_folder/{current_user.id}/", 
                public_id = f"add-to-cart{page_id}")

                Cloud.uploader.upload("./click-checkout-button.png", 
                folder = f"my_folder/{current_user.id}/", 
                public_id = f"click-checkout-button{page_id}")
              
                Cloud.uploader.upload("./clickpaymentbutton.png", 
                folder = f"my_folder/{current_user.id}/", 
                public_id = f"clickpaymentbutton{page_id}")

                Cloud.uploader.upload("./product-page.png", 
                folder = f"my_folder/{current_user.id}/", 
                public_id = f"product-page{page_id}")

                Cloud.uploader.upload("./person-information.png", 
                folder = f"my_folder/{current_user.id}/", 
                public_id = f"person-information{page_id}")


                time.sleep(20)

                print(page_id,current_user.id)
                type_payment_info= Cloud.CloudinaryImage(f"my_folder/{current_user.id}/type-payment-info{page_id}.png")
                click_checkout_button= Cloud.CloudinaryImage(f"my_folder/{current_user.id}/click-checkout-button{page_id}.png")
                personal_info_image= Cloud.CloudinaryImage(f"my_folder/{current_user.id}/person-information{page_id}.png")
                add_tocart_image= Cloud.CloudinaryImage(f"my_folder/{current_user.id}/add-to-cart{page_id}.png")
                click_payment_button_image= Cloud.CloudinaryImage(f"my_folder/{current_user.id}/clickpaymentbutton{page_id}.png")
                product_page_image= Cloud.CloudinaryImage(f"my_folder/{current_user.id}/product-page{page_id}.png")

                print(type_payment_info.url)
                print(click_checkout_button.url)
                print(personal_info_image.url)
                print(add_tocart_image.url)
                print(click_payment_button_image.url)
                print(product_page_image.url)



                requests.post("https://api.mailgun.net/v3/sandbox46bbbb850d304e6396c09ddbb7703a21.mailgun.org/messages",
                auth=("api", "1ea281e23190f090dcfe8d12336cad0c-7bce17e5-9bac263c"),
                data={"from": "Hasan: <postmaster@sandbox46bbbb850d304e6396c09ddbb7703a21.mailgun.org>",
                "to": "phananhtuan1011@gmail.com",
                "subject": "Health Check Results",
                "text": f"This is working",
                "html": f"<html><h1 style='text-align:center'>Health Check Report</h1></br><h3 style='text-align:center'>Product Page</h3><h3>Test Result:{product_page_email}</h3><img src={product_page_image.url} width='1000' height='500'><h3 style='text-align:center'>Click Add to Cart Button<h3><h3>Test Result:{add_to_cart_email}</h3><img src={add_tocart_image.url} width='1000' height='500'/><h3 style='text-align:center'>Type Shipping Info<h3><h3>Test Result:{personal_info_email}</h3><img src={personal_info_image.url} width='1000' height='500'/><h3 style='text-align:center'>Click Checkout Button<h3><h3>Test Result:{checkout_text_email}</h3><img src={click_checkout_button.url} width='1000' height='500'/><h3 style='text-align:center'>Type payment information<h3><h3>Test Result:{payment_info_email}</h3><img src={type_payment_info.url} width='1000' height='500'/><h3 style='text-align:center'>Click Payment button<h3><h3>Test Result:{payment_button_email}</h3><img src={click_payment_button_image.url} width='1000' height='500'/><html/>"})
                print("send email")
        #3 enter personal info
        def personalInfo(go_product_page,add_to_cart,checkout_test):
            try:
                time.sleep(5)
                xpath="//input[contains(@placeholder, 'Email')]"
                driver.find_element_by_xpath(xpath).send_keys("abc123@hotmail.com")
                time.sleep(3)
                
                xpath="//input[contains(@placeholder,'First name')]"
                firstname= driver.find_element_by_xpath(xpath)
                firstname.send_keys("Hasan")
                print("type first name")
                time.sleep(3)

                xpath="//input[contains(@placeholder,'Last name')]"
                lastname= driver.find_element_by_xpath(xpath)
                lastname.send_keys("Armstrong")
                print("print last name")
                time.sleep(3)

                xpath="//input[contains(@placeholder,'Address')]"
                # formatXpath= xpath.format(address)
                testaddress= driver.find_element_by_xpath(xpath)
                testaddress.send_keys("12 Copac Square")
                print("print address")
                time.sleep(3)

                xpath="//input[contains(@placeholder,'City')]"
                testcity= driver.find_element_by_xpath(xpath)
                testcity.send_keys("London")
                print("print city")
                time.sleep(3)

                xpath="//input[contains(@placeholder,'Postal code')]"
                testpost_code= driver.find_element_by_xpath(xpath)
                testpost_code.send_keys("111111")
                print("print post code")
                time.sleep(3)
                driver.save_screenshot("person-information.png")
                # go to shipping page
                # xpath= "//span[contains(text(),'Continue to shipping method')]"
                driver.find_element_by_id("continue_button").click()
                time.sleep(2)
                driver.save_screenshot("click-checkout-button.png")
                print("click continue to shipping info button")
                personal_info= True
                time.sleep(5)
                payment(go_product_page,add_to_cart,checkout_test,personal_info)
            except NoSuchElementException:
                personal_info= False
                payment(go_product_page,add_to_cart,checkout_test,personal_info)
                print("personal info form input didn't work")





            

        #2) Go to checkout
        def checkout(go_product_page, add_to_cart):
            print(checkout_text)
            print("run checkout")
        #go to checkout 
            try:
                time.sleep(3)
                xpath="//a[contains(@value,'{0}')]"
                formatXpath= xpath.format(checkout_text)
                go_to_checkout_a= driver.find_element_by_xpath(formatXpath).click()
                time.sleep(3)
                driver.save_screenshot("checkout.png")
                time.sleep(4)
                checkout= True
                personalInfo(go_product_page, add_to_cart, checkout)
            except NoSuchElementException:
                try:
                    time.sleep(3)
                    xpath="//input[contains(@value,'{0}')]"
                    formatXpath= xpath.format(checkout_text)
                    #check if element is clickable
                    if element_to_be_clickable(formatXpath):
                        print("element is found and can be clicked")
                        driver.find_element_by_xpath(formatXpath).click()
                        driver.save_screenshot("personal-information.png")
                        time.sleep(2)
                        checkout= True
                        personalInfo(go_product_page, add_to_cart, checkout)
                except NoSuchElementException:
                    try:
                        time.sleep(3)
                        xpath="//span[contains(@value,'{0}')]"
                        formatXpath= xpath.format(checkout_text)
                        go_to_checkout_span= driver.find_element_by_xpath(formatXpath).click()
                        time.sleep(3)
                        print("span tag with {0}")
                        driver.save_screenshot("checkout.png")
                        checkout= True
                        personalInfo(go_product_page, add_to_cart, checkout)
                    except NoSuchElementException:
                        try:
                            time.sleep(3)
                            xpath="//div[contains(@value,'{0}')]"
                            formatXpath= xpath.format(checkout_text)
                            driver.find_element_by_xpath(formatXpath).click()
                            time.sleep(3)
                            cart_button.click()
                            print("div tag with {0}")
                            driver.save_screenshot("checkout.png")
                            print(go_to_checkout_div)
                            checkout= True
                            personalInfo(go_product_page, add_to_cart, checkout)
                            time.sleep(5)
                        except NoSuchElementException:
                            checkout= False
                            personalInfo(go_product_page, add_to_cart, checkout)
                            print("Can't find checkout button")

        #add to cart
        time.sleep(3)

        print("*****",current_user.id)
        driver.set_window_size(desktop['width'], desktop['height'])
        driver.get(linkWithProtocol)
        go_product_page=True
        time.sleep(5)
        driver.save_screenshot("product-page.png")
        
    
        # 1) Find cart INPUT element with text/value
        try:
            xpath="//span[contains(text(),'{0}')]"
            formatXpath= xpath.format(cart_text)
            if element_to_be_clickable(formatXpath):
                print("found cart span with tag name input with text")
                driver.find_element_by_xpath(formatXpath).click()
                time.sleep(3)
                driver.save_screenshot("add-to-cart.png")
                add_to_cart= True
                checkout(go_product_page,add_to_cart)
        except NoSuchElementException:
            try:
                xpath="//input[contains(@value,'{0}')]"
                formatXpath= xpath.format(cart_text)
                if element_to_be_clickable(formatXpath):
                    driver.find_element_by_xpath(formatXpath).click()
                    time.sleep(3)
                    driver.save_screenshot("add-to-cart.png")
                    print("found cart button with input value")
                    add_to_cart= True
                    checkout(go_product_page,add_to_cart)
            except NoSuchElementException:
                # Find cart BUTTON element with text/value
                try:
                    xpath="//button[contains(text(),'{0}')]"
                    formatXpath= xpath.format(cart_text)
                    driver.find_element_by_xpath(formatXpath).click()
                    time.sleep(3)
                    driver.save_screenshot("add-to-cart.png")
                    print("found cart button with tag name button with text")
                    add_to_cart= True
                    checkout(go_product_page,add_to_cart)
                except NoSuchElementException:
                    try: 
                        xpath="//button[contains(@value,'{0}')]"
                        formatXpath= xpath.format(cart_text)
                        driver.find_element_by_xpath(formatXpath).click()
                        time.sleep(3)
                        driver.save_screenshot("add-to-cart.png")
                        print("found cart button with button value")
                        add_to_cart= True
                        checkout(go_product_page,add_to_cart)
                    except NoSuchElementException:
                        # Find cart SPAN element element with text/value
                        try:
                            xpath="//span[contains(text(),'{0}')]"
                            formatXpath= xpath.format(cart_text)
                            driver.find_element_by_xpath(formatXpath).click()
                            time.sleep(3)
                            driver.save_screenshot("add-to-cart.png")
                            print("found cart button with tag name span with text")
                            add_to_cart= True
                            checkout(go_product_page,add_to_cart)
                        except NoSuchElementException:
                            try:
                                xpath="//div[contains(text(),'{0}')]"
                                formatXpath= xpath.format(cart_text)
                                driver.find_element_by_xpath(formatXpath).click()
                                time.sleep(3)
                                driver.save_screenshot("add-to-cart.png")
                                print("found cart button with tag name div with text")
                                add_to_cart= True
                                checkout(go_product_page,add_to_cart)
                            except NoSuchElementException:
                                try:
                                    xpath="//span[contains(@value,'{0}')]"
                                    formatXpath= xpath.format(cart_text)
                                    driver.find_element_by_xpath(formatXpath).click()
                                    time.sleep(3)
                                    driver.save_screenshot("add-to-cart.png")
                                    print("found cart button with span value")
                                    add_to_cart= True
                                    checkout(go_product_page,add_to_cart)
                                except NoSuchElementException:
                                    add_to_cart= False
                                    checkout(go_product_page,add_to_cart)
                                    print("Could not find add to cart element")
          
        
                

       

