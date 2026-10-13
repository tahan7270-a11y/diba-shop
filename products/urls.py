from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('search/', views.search, name='search'),                    # ← این خط
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]