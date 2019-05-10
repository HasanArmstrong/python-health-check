
# This will work using headless Chrome for any Desktop OS (Windows, MacOS, Linux Desktop)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import platform
import time
from selenium.webdriver.support import expected_conditions as EC


def run_check(url):
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
        driver.set_window_size(desktop['width'], desktop['height'])
        driver.get(linkWithProtocol)
        time.sleep(5)
        driver.save_screenshot("product_page.png")

        #close pop up


        #add to cart
        driver.set_window_size(desktop['width'], desktop['height'])
        driver.get(linkWithProtocol)
        time.sleep(1)
        
        elementByName=driver.find_element_by_id("AddToCartForm")
        # driver.execute_script("arguments[0].scrollIntoView(true);", elementByName)
        time.sleep(3)
        find_cart=driver.find_element_by_xpath("//span[text()='Add to cart']")
        print("****", find_cart)
        time.sleep(2)
        find_cart.click()
        if find_cart is not None:
            print("We found an element by Xpath")
        else:
                print("error")
        time.sleep(5)
        driver.save_screenshot("add_to_cart.png")
        time.sleep(5)

        #go to checkout
        # cart_button=driver.find_element_by_name("checkout")
        # cart_button.click()
        # time.sleep(5)
        # driver.save_screenshot("checkout.png")
       
       #Fill out checkout payment form
        # time.sleep(7)
        # driver.find_element_by_id("checkout_email").send_keys("abc@hotmail.com")
        # time.sleep(2)
        # driver.find_element_by_id("checkout_shipping_address_first_name").send_keys("david")
        # time.sleep(2)
        # driver.find_element_by_id("checkout_shipping_address_last_name").send_keys("Hasslehof")
        # time.sleep(2)
        # driver.find_element_by_id("checkout_shipping_address_address1").send_keys("12 Copac Square")
        # time.sleep(2)
        # driver.find_element_by_id("checkout_shipping_address_city").send_keys("Saigon")
        # time.sleep(2)
        # driver.find_element_by_id("checkout_shipping_address_zip").send_keys("111111")
        # time.sleep(2)
        # driver.find_element_by_id("checkout_shipping_address_phone").send_keys("09117858232")
        # time.sleep(5)
        # driver.find_element_by_id("continue_button").click()
        # driver.save_screenshot("personal-information.png")
        # set the window size for tablet
        #     driver.set_window_size(tablet['width'], tablet['height'])
        #     driver.get(linkWithProtocol)
        #     time.sleep(2)
        #     driver.save_screenshot(tablet['output'])

        # set the window size for mobile
        #     driver.set_window_size(mobile['width'], mobile['height'])
        #     driver.get(linkWithProtocol)
        #     time.sleep(2)
        #     driver.save_screenshot(mobile['output'])
            