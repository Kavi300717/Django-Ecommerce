from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Product
from category.models import category
from carts.models import CartItem
from carts.views import _cart_id

# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        # get the cart item for this product (if any) for the current session
        cart_item = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).first()
    except Exception as e:
        raise e
    
    
    context = {
        'single_product': single_product,
        'cart_item': cart_item,
    }
    return render(request, 'store/product_detail.html', context)