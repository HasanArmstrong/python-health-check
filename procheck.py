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

def proplan():
    print("this is working")
    # # Gets the path to the right chromedriver
    # time.sleep(10)
    # path = "$PATH:/Users/pc/Desktop/shophealthcheck" + platform.system()
    # links = [url]
    # options = webdriver.ChromeOptions()
    # # options.add_argument("headless")
    # # must install linux browser `sudo apt-get install -y chromium-browser` in Linux
    # if(platform.system() == 'Linux'):
    #     options.binary_location = '/usr/bin/chromium-browser'
    # options.add_argument("disable-infobars")  # disabling infobars
    # options.add_argument("--disable-extensions")  # disabling extensions
    # options.add_argument("--disable-gpu")  # applicable to windows os only
    # # overcome limited resource problems
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--no-sandbox")  # Bypass OS security model
    # # Thanks to https://stackoverflow.com/a/50642913/2291648 for explaining the arguments above

    # with webdriver.Chrome("chromedriver", chrome_options=options) as driver:
    #     # these values represent the sizes of the entire browser window and not the viewport.
    #     for link in links:
    #         desktop = {'output': str(link) + '-desktop.png',
    #                 'width': 2200,
    #                 'height': 1800}
    #         tablet = {'output': str(link) + '-tablet.png',
    #                 'width': 1200,
    #                 'height': 1400}
    #         mobile = {'output': str(link) + '-mobile.png',
    #                 'width': 680,
    #                 'height': 1200}
    #         linkWithProtocol = 'https://' + str(link)

    # #add to cart
    # time.sleep(3)

    # # print("*****",current_user.id)
    # driver.set_window_size(desktop['width'], desktop['height'])
    # driver.get(linkWithProtocol)
    # go_product_page=True
    # time.sleep(5)
    # driver.save_screenshot("pro-product-page.png")