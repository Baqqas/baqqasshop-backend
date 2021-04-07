from django.urls import path
from .views import Index, Update


app_name = 'profiles'


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('update/', Update.as_view(), name='update'),
]
