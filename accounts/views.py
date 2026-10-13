from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
# from django_ratelimit.decorators import ratelimit


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            messages.error(request, 'رمز عبور و تکرار آن یکسان نیستند.')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'این نام کاربری قبلاً استفاده شده است.')
            return render(request, 'accounts/register.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=user, phone=phone)
        
        login(request, user)
        return redirect('home')
    
    return render(request, 'accounts/register.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        
        # اگه گزینه ۱ رو انتخاب کردی:
        # user.username = request.POST.get('username')
        # user.email = request.POST.get('email')
        
        # اگه گزینه ۲ رو انتخاب کردی:
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.save()
        
        # پروفایل
        profile = user.profile
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.postal_code = request.POST.get('postal_code', '')
        
        if request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        messages.success(request, 'اطلاعات با موفقیت ذخیره شد.')
        return redirect('profile')
    
    return render(request, 'accounts/profile.html')