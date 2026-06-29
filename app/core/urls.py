from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/csv/', include('csvapi.urls')),
    path('product/', include('product.urls')),
    path('api/auth/', include('accounts.urls')),
]
