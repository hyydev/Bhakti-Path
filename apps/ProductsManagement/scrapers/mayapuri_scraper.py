from .base_scraper import BaseScraper
from .utils import download_image_and_save
from apps.ProductsManagement.models import Product, Category
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class MayapuriScraper(BaseScraper):
    def scrape(self):
        product_urls = [
            'https://thevrindastore.com/products/1-round-radha-name-original-tulsi-mala',
        ]
        
        try:
            for url in product_urls:
                try:
                    print(f"Processing URL: {url}")
                    self.driver.get(url)
                    
                    # Wait for page to load completely
                    time.sleep(3)  # Initial wait
                    
                    # Set longer timeout and more robust element finding
                    wait = WebDriverWait(self.driver, 20)
                    
                    try:
                        # Try to find title - using more generic selector
                        title = wait.until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "h1.ProductDetailsMainCard__ProductName-sc-1rhvpxz-7, h1.product-title")
                        )).text
                        print(f"Found title: {title}")
                    except TimeoutException:
                        print("Could not find title element")
                        continue
                    
                    try:
                        # Try multiple possible price selectors
                        price_element = wait.until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "span.ProductDetailsMainCard__DiscountedPrice-sc-1rhvpxz-17, span.discounted-price, span.price")
                        ))
                        price = price_element.text.replace("₹", "").replace(",", "").strip()
                        print(f"Found price: {price}")
                    except TimeoutException:
                        print("Could not find price element")
                        continue
                    
                    try:
                        # Try multiple description selectors
                        desc = wait.until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div.ProductDetailsMainCard__Description-sc-1rhvpxz-12, div.product-description, meta[name='description']")
                        ))
                        if desc.tag_name == "meta":
                            desc_text = desc.get_attribute("content")
                        else:
                            desc_text = desc.text
                        print(f"Found description")
                    except TimeoutException:
                        desc_text = "No description available"
                        print("Could not find description element")
                    
                    try:
                        # Image with fallback
                        img_element = wait.until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "img.ProductMainSlider__ProductImage-sc-1b8icty-2, img.product-image")
                        ))
                        img_url = img_element.get_attribute("src")
                        print(f"Found image URL: {img_url}")
                    except TimeoutException:
                        img_url = None
                        print("Could not find image element")
                    
                    # Create/update product
                    try:
                        category, _ = Category.objects.get_or_create(name="Mala")
                        product, _ = Product.objects.update_or_create(
                            source_url=url,
                            defaults={
                                'title': title,
                                'description': desc_text,
                                'price': price,
                                'stock_status': 'IN_STOCK',
                                'category': category,
                            }
                        )
                        
                        if img_url:
                            download_image_and_save(product, img_url)
                        
                        print(f"Successfully saved product: {title}")
                        
                    except Exception as e:
                        print(f"Error saving product to database: {str(e)}")
                        
                except Exception as e:
                    print(f"Error processing URL {url}: {str(e)}")
                    continue
                    
        finally:
            # Ensure browser is properly closed
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
                print("Browser closed")