from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Product, Variation
from category.models import category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': page_products,
        'product_count': product_count,
        'paginator': paginator,
        'page_obj': page_products,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        # get the cart item for this product (if any) for the current session
        cart_item = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).first()
        # get all size and color variations for this product
        product_variations = Variation.objects.filter(product=single_product, is_active=True)
        print(f"Total variations for {single_product.product_name}: {product_variations.count()}")
        print(f"All variations: {product_variations.values_list('variation_category', 'variation_value')}")
        
        colors = product_variations.filter(variation_category='color').values_list('variation_value', flat=True).distinct()
        sizes = product_variations.filter(variation_category='size').values_list('variation_value', flat=True).distinct()
        
        print(f"Colors: {list(colors)}")
        print(f"Sizes: {list(sizes)}")
    except Exception as e:
        raise e
    
    
    context = {
        'single_product': single_product,
        'cart_item': cart_item,
        'colors': colors,
        'sizes': sizes,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
        context = {
            'products': products,
            'product_count': product_count,
        }    
        
    return render(request, 'store/store.html', context)