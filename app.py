from selenium import webdriver
import time
from flask import Flask, render_template

app= Flask(__name__)

@app.route('/')
def index():
    return render_template('landingpage.html')

if __name__ == '__main__':
    app.run()





# collection_page_link= input("Please provide your Shopify page url:")

# options = webdriver.ChromeOptions() # define options
# options.add_argument("headless") 

# links = [collection_page_link]

# with webdriver.Chrome("/Users/pc/Desktop/shophealthcheck/chromedriver", chrome_options=options) as driver:
#     for link in links:
#         desktop = {'output': str(link) + '-desktop.png',
#                    'width': 2200,
#                    'height': 1800}
#         tablet = {'output': str(link) + '-tablet.png',
#                   'width': 1200,
#                   'height': 1400}
#         mobile = {'output': str(link) + '-mobile.png',
#                   'width': 680,
#                   'height': 1200}

#         linkWithProtocol = 'https://' + str(link)

#         # set the window size for desktop
#         driver.set_window_size(desktop['width'], desktop['height'])
#         driver.get(linkWithProtocol)
#         time.sleep(2)
#         driver.save_screenshot(desktop['output'])
#          # set the window size for tablet
#         driver.set_window_size(tablet['width'], tablet['height'])
#         driver.get(linkWithProtocol)
#         time.sleep(2)
#         driver.save_screenshot(tablet['output'])


