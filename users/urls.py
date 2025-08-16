from django.urls import path
from users import views

urlpatterns = [
    path('oqituvchilar/', views.admin_oqituvchilar, name='admin_oqituvchilar'),
    path('oqituvchi_create/', views.oqituvchi_create, name='oqituvchi_create'),
    path('oqituvchi_update/<str:pk>/', views.oqituvchi_update, name='oqituvchi_update'),
    path('oqituvchi_delete/<str:pk>/', views.oqituvchi_delete, name='oqituvchi_delete'),

    path('fakultetlar/', views.admin_fakultetlar, name='admin_fakultetlar'),
    path('fakultetlar_create/', views.fakultet_create, name='fakultet_create'),
    path('fakultetlar_update/<str:pk>/', views.fakultet_update, name='fakultet_update'),
    path('fakultetlar_delete/<str:pk>/', views.fakultet_delete, name='fakultet_delete'),

    path('yonalishlar/', views.admin_yonalishlar, name='admin_yonalishlar'),
    path('yonalishlar_create/', views.yonalish_create, name='yonalish_create'),
    path('yonalishlar_update/<str:pk>/', views.yonalish_update, name='yonalish_update'),
    path('yonalishlar_delete/<str:pk>/', views.yonalish_delete, name='yonalish_delete'),

    path('kurslar/', views.admin_kurslar, name='admin_kurslar'),
    path('kurslar_create/', views.kurs_create, name='kurs_create'),
    path('kurslar_update/<str:pk>/', views.kurs_update, name='kurs_update'),
    path('kurslar_delete/<str:pk>/', views.kurs_delete, name='kurs_delete'),

    path('guruhlar/', views.admin_guruhlar, name='admin_guruhlar'),
    path('guruhlar_create/', views.guruh_create, name='guruh_create'),
    path('guruhlar_update/<str:pk>/', views.guruh_update, name='guruh_update'),
    path('guruhlar_delete/<str:pk>/', views.guruh_delete, name='guruh_delete'),
    
    path('natijalar/', views.admin_natijalar, name='admin_natijalar'),
    path('get-yonalishlar/', views.get_yonalishlar, name='get_yonalishlar'),
    path('chiqish/', views.chiqish_user, name='chiqish_user'),
]