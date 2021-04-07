from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('baqqasadmin/', admin.site.urls),
    path('api/users/', include('users.urls', namespace='users')),
    path('api/products/', include('products.urls', namespace='products')),
    path('api/orders/', include('orders.urls', namespace='orders')),
    path('api/users/profile/', include('profiles.urls', namespace='profile'))
]
