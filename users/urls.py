from django.urls import path
from .views import Index, Create, Show, Update, Delete, MyTokenObtainPairView


app_name = 'users'


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', Create.as_view(), name='create'),
    path('<int:id>/', Show.as_view(), name='show'),
    path('update/<int:id>/', Update.as_view(), name='update'),
    path('delete/<int:id>/', Delete.as_view(), name='delete')
]
