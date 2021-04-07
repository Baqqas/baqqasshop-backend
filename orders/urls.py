from django.urls import path
from .views import Index, Create, MyOrders, Show, Pay, Deliver


app_name = 'orders'


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('add/', Create.as_view(), name='create'),
    path('myorders/', MyOrders.as_view(), name='myorders'),
    path('<int:pk>/', Show.as_view(), name='show'),
    path('<int:pk>/pay/', Pay.as_view(), name='pay'),
    path('<int:pk>/deliver/', Deliver.as_view(), name='deliver'),
]
