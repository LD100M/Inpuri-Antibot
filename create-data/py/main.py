from selenium import webdriver
import time

# Set Chrome options
opts = webdriver.ChromeOptions()
opts.headless = False
opts.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'

# Initialize the Chrome WebDriver
driver = webdriver.Chrome( options=opts)

# Navigate to the desired web page
driver.get('http://127.0.0.1:3000/site/login.html')

# Wait for 60 seconds
time.sleep(60)

# Close the browser
driver.quit()
