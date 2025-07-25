from django.db import models
from django.utils.text import slugify
from apps.User.models import Baseclass
from django.utils.crypto import get_random_string

class Product(Baseclass):
    PRODUCT_TYPES = [
    ('MALA', 'Mala / Tulsi Kanthi'),
    ('JAPA', 'Japa Beads / Bags'),
    ('TILAK', 'Tilak / Gopi Chandan'),
    ('CHANDAN', 'Chandan Paste / Powder'),
    ('BOOK', 'Books (Spiritual / Srila Prabhupada)'),
    ('DECOR', 'Temple Decor / Home Altar Items'),
    ('MUSIC', 'Spiritual CDs / Kirtan'),
    ('DRESS', 'Deity Dresses / Accessories'),
    ('PUJA', 'Puja Samagri / Aarti Items'),
    ('ABHISHEK', 'Abhishek Items / Panchamrit Sets'),
    ('FOOD', 'Dry Fruits / Bhog Items / Mishri'),
    ('GIFT', 'Spiritual Gifts / Hampers'),
    ('UTENSILS', 'Copper / Brass Puja Utensils'),
    ('FESTIVAL', 'Ekadashi / Janmashtami Items'),
    ('OTHER', 'Other Items'),

    ]

    # Basic Info
    title = models.CharField(max_length=255)
    sku = models.CharField(max_length=100,unique=True,blank=True)
    slug = models.SlugField(unique=True,blank=True)  # For SEO-friendly URLs
    description = models.TextField(blank=True, null=True)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES, default='OTHER')
    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE, blank=True, null=True)

    # Price & Stock
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    stock_quantity = models.IntegerField(default=0)

    # Meta / SEO
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.JSONField(default=list, blank=True)  # e.g. ["tulsi", "beads", "japa"]

    # Source Info
    source_url = models.URLField(unique=True,blank=True,null=True)
    source_website = models.CharField(max_length=100, blank=True, null=True)  # e.g. 'mayapuri'

   

    class Meta:
        ordering = ['-created_at']
    
    def generate_unique_sku(self, title):
        base_sku = title[:3].upper()
        while True:
            sku = f"{base_sku}-{get_random_string(6).upper()}"
            if not Product.objects.filter(sku=sku).exists():
                return sku


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.sku:
            self.sku = self.generate_unique_sku(title=self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



class ProductImage(Baseclass):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    is_primary = models.BooleanField(default=False)


class Category(Baseclass):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True,blank=True)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='category-icons/', blank=True, null=True)  # Optional
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

    