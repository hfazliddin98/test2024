from django.urls import path
from .views import home, kirish, chiqish, mavzular, mavzu, testlar, test, natijalar, test_bajarish  

urlpatterns = [
    path('', home, name='home'),
    path('kirish/', kirish, name='kirish'),
    path('chiqish/', chiqish, name='chiqish'),
    path('mavzular/', mavzular, name='mavzular'),
    path('mavzu/', mavzu, name='mavzu'),
    path('testlar/', testlar, name='testlar'),
    path('test/', test, name='test'),
    path('natijalar/', natijalar, name='natijalar'),
    path('test_bajarish/<int:str>/', test_bajarish, name='test_bajarish'),
]