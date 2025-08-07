import os
import random
import sys
from faker import Faker
from django.core.files import File

# Setup Django
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, PROJECT_ROOT)  # Insert at beginning for priority
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BhaktiVerse.settings")

import django
django.setup()

# Import models after Django setup
from apps.ProductsManagement.models import Product, Category, ProductImage

fake = Faker()

Category_names = [ 
    "Mala",
    "Japa Beads",
    "Tilak",
    "Chandan Paste",
    "Books",
    "Temple Decor",
    "Spiritual CDs",
    "Deity Dresses",
    "Puja Samagri",
    "Abhishek Items",
    "Dry Fruits",
    "Spiritual Gifts",
    "Puja Utensils",
    "Festival Items",
    "Other"
]

categories = []

# ✅ Create categories
for name in Category_names:
    category, created = Category.objects.get_or_create(name=name, defaults={
        'slug': name.lower().replace(' ', '-'),
    })
    categories.append(category)

print(f"{len(categories)} categories created.")

# ✅ Get image files
IMAGE_FOLDER = 'apps/ProductsManagement/media/product_images'
image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

# ✅ Create products
for category in categories:
    for i in range(10):
        title = fake.unique.sentence(nb_words=3)
        price = round(random.uniform(100.0, 9999.99), 2)
        description = fake.paragraph(nb_sentences=5)
        slug = '-'.join(title.lower().split())
        sku = f"SKU-{random.randint(100000, 999999)}"

        product = Product.objects.create(
            title=title,
            slug=slug,
            description=description,
            price=price,
            category=category,
            sku=sku
        )

        # ✅ Add 1–3 images per product
        selected_images = random.sample(image_files, k=random.randint(1, 3))
        for idx, img_name in enumerate(selected_images):
            with open(os.path.join(IMAGE_FOLDER, img_name), 'rb') as f:
                ProductImage.objects.create(
                    product=product,
                    image=File(f, name=img_name),
                    alt_text=f"{title} image {idx+1}",
                    is_primary=(idx == 0)
                )

        print(f"✅ Product '{product.title}' created in category '{category.name}' with {len(selected_images)} images.")
