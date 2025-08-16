from django.urls import path

from .views import home, kirish, chiqish, mavzu, test, test_bajarish, mavzu_qrcode, mavzu_edit, mavzu_delete, test_delete, test_edit
import quiz.views as views

urlpatterns = [
    path('', home, name='home'),
    path('kirish/', kirish, name='kirish'),
    path('chiqish/', chiqish, name='chiqish'),
    path('mavzu/', mavzu, name='mavzu'),
    path('mavzu/<str:pk>/', mavzu, name='mavzu_detail'),
    path('mavzu/<str:pk>/edit/', mavzu_edit, name='mavzu_edit'),
    path('mavzu/<str:pk>/delete/', mavzu_delete, name='mavzu_delete'),
    path('test/<str:pk>/delete/', test_delete, name='test_delete'),
    path('test/<str:pk>/edit/', test_edit, name='test_edit'),
    path('test/', test, name='test'),
    path('test_bajarish/<str:pk>/', test_bajarish, name='test_bajarish'),
    path('teacher/mavzular/', views.teacher_mavzular, name='teacher_mavzular'),
    path('teacher/testlar/', views.teacher_testlar, name='teacher_testlar'),
    path('teacher/natijalar/', views.teacher_natijalar, name='teacher_natijalar'),
    path('mavzu/<str:pk>/qrcode/', mavzu_qrcode, name='mavzu_qrcode'),
    path('test_bajarish/<str:pk>/', test_bajarish, name='test_bajarish'),
    path('teacher/mavzular/', views.teacher_mavzular, name='teacher_mavzular'),
    path('teacher/testlar/', views.teacher_testlar, name='teacher_testlar'),
    path('teacher/natijalar/', views.teacher_natijalar, name='teacher_natijalar'),
    path('mavzu/<str:pk>/qrcode/', mavzu_qrcode, name='mavzu_qrcode'),
]