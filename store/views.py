from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Product
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
    except Exception as e:
        raise e
    
    
    context = {
        'single_product': single_product,
        'cart_item': cart_item,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
        context = {
            'products': products,
        }    
        
    return render(request, 'store/store.html', context)