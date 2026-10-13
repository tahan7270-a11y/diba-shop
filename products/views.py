from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category


def product_list(request):
    """لیست همه‌ی محصولات با فیلتر و مرتب‌سازی"""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True, parent=None)
    
    # ===== فیلتر دسته‌بندی =====
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # ===== فیلتر قیمت =====
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price:
        products = products.filter(price__gte=int(min_price))
    if max_price:
        products = products.filter(price__lte=int(max_price))
    
    # ===== فیلتر موجودی =====
    in_stock = request.GET.get('in_stock')
    if in_stock == '1':
        products = products.filter(is_active=True)
    
    # ===== مرتب‌سازی =====
    sort = request.GET.get('sort', 'newest')
    
    if sort == 'cheapest':
        products = products.order_by('price')
    elif sort == 'most_expensive':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    elif sort == 'oldest':
        products = products.order_by('created_at')
    elif sort == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')
    
    context = {
        'products': products,
        'categories': categories,
        'sort': sort,
        'selected_category': category_slug,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'products/product_list.html', context)
def category_products(request, slug):
    """محصولات یک دسته"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'products/category_products.html', context)


def product_detail(request, slug):
    """جزئیات محصول"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)


def search(request):
    """جستجوی محصولات"""
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(is_active=True)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    else:
        products = Product.objects.none()
    
    context = {
        'query': query,
        'products': products,
        'result_count': products.count(),
    }
    return render(request, 'products/search.html', context)