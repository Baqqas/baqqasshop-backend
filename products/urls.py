from django.urls import path
from .views import Index, Create, Show, Update, Delete, \
    UploadImage, CreateReview, TopProducts


app_name = 'products'


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('top/', TopProducts.as_view(), name='top'),
    path('create/', Create.as_view(), name='create'),
    path('upload/', UploadImage.as_view(), name='upload'),
    path('<int:pk>/', Show.as_view(), name='show'),
    path('update/<int:pk>/', Update.as_view(), name='update'),
    path('delete/<int:pk>/', Delete.as_view(), name='delete'),
    path('<int:pk>/reviews/', CreateReview.as_view(), name='review')
]
