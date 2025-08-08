import os
import sys
import django

# Django Setup
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BhaktiVerse.settings")
django.setup()

# Now import models
from apps.ProductsManagement.models import Product, Inventory
from django.db import transaction
import random

@transaction.atomic
def create_inventories():
    products = Product.objects.all()
    created = 0
    skipped = 0

    for product in products:
        if not hasattr(product, "inventory"):
            quantity = random.randint(5, 100)  # Random stock
            Inventory.objects.create(
                product=product,
                quantity=quantity,
                is_in_stock=True if quantity > 0 else False
            )
            created += 1
        else:
            skipped += 1

    print(f"✅ Inventory Created for {created} products")
    print(f"⚠️ Already had inventory: {skipped} products")

if __name__ == "__main__":
    create_inventories()
