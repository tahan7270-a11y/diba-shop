import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from cart.views import get_or_create_cart
from products.models import Product
from .models import Order, OrderItem


@login_required
def checkout(request):
    """ثبت سفارش"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.warning(request, 'سبد خرید شما خالی است.')
        return redirect('cart_view')
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        postal_code = request.POST.get('postal_code', '')
        
        # چک کردن اطلاعات
        if not all([full_name, phone, address]):
            messages.error(request, 'لطفاً همه‌ی فیلدهای اجباری را پر کنید.')
            return render(request, 'orders/checkout.html', {
                'cart': cart,
                'cart_items': cart_items,
            })
        
        # ساخت شماره سفارش
        order_number = f"DB{random.randint(100000, 999999)}"
        
        # ساخت سفارش
        order = Order.objects.create(
            user=request.user,
            order_number=order_number,
            full_name=full_name,
            phone=phone,
            address=address,
            postal_code=postal_code,
            total_price=cart.total_price,
            status='pending',
        )
        
        # اضافه کردن آیتم‌ها
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.final_price,
                quantity=item.quantity,
                size=item.size,
                color=item.color,
            )
        
        # پاک کردن سبد خرید
        cart.items.all().delete()
        
        messages.success(request, f'سفارش {order_number} با موفقیت ثبت شد.')
        return redirect('order_success', order_number=order_number)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_success(request, order_number):
    """صفحه‌ی موفقیت سفارش"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/success.html', {'order': order, 'order_number': order_number})


@login_required
def my_orders(request):
    """سفارش‌های من"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})