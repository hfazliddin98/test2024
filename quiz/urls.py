from django.urls import path
from .views import home, kirish, chiqish, mavzular, mavzu, testlar, test, natijalar, test_bajarish, take_test  

urlpatterns = [
    path('', home, name='home'),
    path('kirish/', kirish, name='kirish'),
    path('chiqish/', chiqish, name='chiqish'),
    path('mavzular/', mavzular, name='mavzular'),
    path('mavzu/', mavzu, name='mavzu'),
    path('testlar/', testlar, name='testlar'),
    path('test/', test, name='test'),
    path('natijalar/', natijalar, name='natijalar'),
    path('test_bajarish/<str:pk>/', test_bajarish, name='test_bajarish'),
    path('take_test/<str:pk>/', take_test, name='take_test')
]