from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/csv/', include('app.csvapi.urls')),
    path('product/', include('app.product.urls')),
    path('api/auth/', include('app.accounts.urls')),
]
