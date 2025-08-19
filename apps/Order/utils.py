from django.core.cache import cache
from decimal import Decimal
from .models import Cart

CART_CACHE_TTL = 60 * 60  # 1 hour


def cart_cache_key(user_id: int) -> str:
    return f"cart_{user_id}"


def decimal_to_str(d: Decimal) -> str:
    # Always convert Decimal to string for JSON safety
    return format(d, 'f')


def build_cart_payload(cart: Cart) -> dict:
    # Optimize queries: load user + cart items + product in one go
    cart = (
        Cart.objects
        .select_related("user")
        .prefetch_related("cart_item__product")
        .get(id=cart.id)
    )

    items = []
    total = Decimal('0')

    for ci in cart.cart_item.all():
        item_total = ci.price_at_time * ci.quantity
        total += item_total

        item = {
            "id": ci.id,
            "product_id": ci.product_id,
            "product_name": ci.product.title,
            "product_price": decimal_to_str(ci.price_at_time),
            "quantity": ci.quantity
        }
        items.append(item)

    payload = {
        "cart": {
            "id": cart.id,
            "user": cart.user.full_name,
            "total_price": decimal_to_str(total),
            "items": items,
        }
    }
    return payload


def get_cart_from_cache(user_id: int):
    return cache.get(cart_cache_key(user_id))


def set_cart_cache(user_id: int, payload: dict):
    cache.set(cart_cache_key(user_id), payload, timeout=CART_CACHE_TTL)


def delete_cart_cache(user_id: int):
    cache.delete(cart_cache_key(user_id))
