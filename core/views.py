from django.shortcuts import render
from .models import Banner
from products.models import Product, Category


def home(request):
    banners = Banner.objects.filter(is_active=True)
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    categories = Category.objects.filter(is_active=True, parent=None)
    
    context = {
        'banners': banners,
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)