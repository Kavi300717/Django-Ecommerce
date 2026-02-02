from .models import Cart, CartItem


def counter(request):
    """Return total quantity of active cart items for current session cart."""
    cart_count = 0
    try:
        cart_id = request.session.session_key
        if not cart_id:
            cart_id = request.session.create()
            cart_id = request.session.session_key

        cart = Cart.objects.filter(cart_id=cart_id).first()
        if cart:
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for item in cart_items:
                cart_count += item.quantity
    except Exception:
        cart_count = 0

    return {'cart_count': cart_count}
