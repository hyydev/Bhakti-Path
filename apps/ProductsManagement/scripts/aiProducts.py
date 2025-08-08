import os
import random
import sys
import json
import openai
from django.core.files import File

# Setup Django
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BhaktiVerse.settings")
import django
django.setup()

# Import models
from apps.ProductsManagement.models import Product, Category, ProductImage

# OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Category list
CATEGORY_NAMES = [
    "Mala", "Japa Beads", "Tilak", "Chandan Paste", "Books",
    "Temple Decor", "Spiritual CDs", "Deity Dresses", "Puja Samagri",
    "Abhishek Items", "Dry Fruits", "Spiritual Gifts", "Puja Utensils",
    "Festival Items", "Other"
]

# Create/Get categories
categories = []
for name in CATEGORY_NAMES:
    category, _ = Category.objects.get_or_create(
        name=name,
        defaults={'slug': name.lower().replace(' ', '-')}
    )
    categories.append(category)

# Image folder path
IMAGE_FOLDER = 'apps/ProductsManagement/media/product_images'
image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

# AI function to generate products for a category
def generate_products_for_category(category_name):
    prompt = f"""
    Generate 10 product ideas for the '{category_name}' category in JSON format.
    Each product must have:
    - title (max 6 words, relevant to '{category_name}')
    - price (random between 100 and 9999)
    - description (2-3 sentences, spiritual/relevant to '{category_name}')
    - sku (unique, starting with 'SKU-')
    Output JSON array only, no extra text.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    try:
        return json.loads(response.choices[0].message["content"])
    except json.JSONDecodeError:
        print(f"⚠ JSON parsing failed for category {category_name}")
        return []

# Create products
for category in categories:
    products_data = generate_products_for_category(category.name)
    for p in products_data:
        product = Product.objects.create(
            title=p['title'],
            slug='-'.join(p['title'].lower().split()),
            description=p['description'],
            price=float(p['price']),
            category=category,
            sku=p['sku']
        )

        # Randomly select 1-3 images from local folder
        selected_images = random.sample(image_files, k=random.randint(1, 3))
        for idx, img_name in enumerate(selected_images):
            with open(os.path.join(IMAGE_FOLDER, img_name), 'rb') as f:
                ProductImage.objects.create(
                    product=product,
                    image=File(f, name=img_name),
                    alt_text=f"{p['title']} image {idx+1}",
                    is_primary=(idx == 0)
                )

        print(f"✅ Product '{product.title}' created in '{category.name}' with {len(selected_images)} images.")
