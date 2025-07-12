import requests
from django.core.files.base import ContentFile
from apps.ProductsManagement.models import ProductImage

def download_image_and_save(product, image_url):
    try:
        img_content = requests.get(image_url).content
        filename = image_url.split("/")[-1]
        img = ProductImage(product=product)
        img.image.save(filename, ContentFile(img_content))
        img.save()
    except Exception as e:
        print(f"Error downloading image: {e}")