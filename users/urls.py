from django.urls import path
from users import views

urlpatterns = [
    path('get-yonalishlar/', views.get_yonalishlar, name='get_yonalishlar'),
]