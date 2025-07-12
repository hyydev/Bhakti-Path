from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os

class BaseScraper:
    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chromedriver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../chromedriver'))
        service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def close(self):
        self.driver.quit()
        
