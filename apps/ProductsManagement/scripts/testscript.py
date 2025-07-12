from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

chrome_options = Options()
chrome_options.add_argument("--headless")

service = Service('../../../chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.google.com")
print("Title:", driver.title)

driver.quit()