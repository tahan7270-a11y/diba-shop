from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from orders.models import Order, OrderItem
from products.models import Product, Category
from accounts.models import Profile
from contact.models import ContactMessage


@staff_member_required
def dashboard(request):
    """داشبورد مدیریت"""
    
    # ===== آمار کلی =====
    total_orders = Order.objects.count()
    total_products = Product.objects.filter(is_active=True).count()
    total_users = Profile.objects.count()
    total_categories = Category.objects.count()
    
    # ===== درآمد کل =====
    total_revenue = Order.objects.filter(
        status__in=['paid', 'processing', 'shipped', 'delivered']
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    # ===== سفارش‌های امروز =====
    today = timezone.now().date()
    today_orders = Order.objects.filter(created_at__date=today).count()
    
    # ===== سفارش‌های در انتظار =====
    pending_orders = Order.objects.filter(status='pending').count()
    
    # ===== پیام‌های خوانده‌نشده =====
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    
    # ===== ۱۰ سفارش آخر =====
    recent_orders = Order.objects.all().order_by('-created_at')[:10]
    
    # ===== پرفروش‌ترین محصولات =====
    top_products = OrderItem.objects.values(
        'product__name', 'product__id'
    ).annotate(
        total_sold=Sum('quantity')
    ).order_by('-total_sold')[:5]
    
    # ===== نمودار فروش ۷ روز اخیر =====
    last_7_days = []
    for i in range(6, -1, -1):
        day = timezone.now().date() - timedelta(days=i)
        count = Order.objects.filter(created_at__date=day).count()
        last_7_days.append({
            'date': day.strftime('%m/%d'),
            'count': count,
        })
    
    context = {
        'total_orders': total_orders,
        'total_products': total_products,
        'total_users': total_users,
        'total_categories': total_categories,
        'total_revenue': total_revenue,
        'today_orders': today_orders,
        'pending_orders': pending_orders,
        'unread_messages': unread_messages,
        'recent_orders': recent_orders,
        'top_products': top_products,
        'last_7_days': last_7_days,
    }
    return render(request, 'dashboard/dashboard.html', context)