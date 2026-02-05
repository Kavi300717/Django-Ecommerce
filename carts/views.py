from django.shortcuts import render, redirect
from store.models import Product, Variation
from .models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    # accept optional size and color from POST (product variants)
    size = None
    color = None
    if request.method == 'POST':
        size = request.POST.get('size') or None
        color = request.POST.get('color') or None

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    # group cart items by product + size + color so variants are separate items
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, size=size, color=color)
        cart_item.quantity += 1
        cart_item.save()
        print(f"✓ Updated Cart: {product.product_name} | Color: {color or 'N/A'} | Size: {size or 'N/A'} | Quantity: {cart_item.quantity}")
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
            size = size,
            color = color,
        )
        cart_item.save()
        print(f"✓ Added to Cart: {product.product_name} | Color: {color or 'N/A'} | Size: {size or 'N/A'} | Quantity: 1")
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    # ensure cart_items is iterable and detect empty cart
    if not cart_items:
        cart_items = []
        cart_is_empty = True
    else:
        cart_is_empty = False

    tax = (2 * total) / 100
    grand_total = total + tax

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'cart_is_empty': cart_is_empty,
    }

    return render(request, 'store/cart.html', context)

def remove_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def checkout(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        if not cart_items:
            return redirect('cart')
    except ObjectDoesNotExist:
        return redirect('cart')

    return render(request, 'store/checkout.html')

def increment_cart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        pass
    # redirect back to `next` if provided, otherwise to cart
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('cart')


def decrement_cart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    # redirect back to `next` if provided, otherwise to cart
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('cart')