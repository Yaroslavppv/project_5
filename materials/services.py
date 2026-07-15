import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(course_title):
    product = stripe.Product.create(name=course_title)
    return product.id


def create_stripe_price(product_id, amount):
    price = stripe.Price.create(
        product=product_id,
        unit_amount=int(amount * 100),
        currency="rub",
    )
    return price.id


def create_stripe_session(price_id):
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.url, session.id
