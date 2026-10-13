from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),           # ← این خط مهمه
    path('orders/', include('orders.urls')),
    path('accounts/', include('accounts.urls')),
    path('about/', include('about.urls')),
    path('contact/', include('contact.urls')),
    path('ai/', include('ai_view.urls')),
    path('dashboard/', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)