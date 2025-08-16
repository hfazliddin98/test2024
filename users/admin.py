from django.contrib import admin
from users.models import Fakultets, Yonalishs, Kurs, Guruhs, Users
from django.contrib.auth.admin import UserAdmin

@admin.register(Users)
class UsersAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    fieldsets = UserAdmin.fieldsets + (
        ('Qo‘shimcha ma’lumot', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Qo‘shimcha ma’lumot', {'fields': ('role',)}),
    )



@admin.register(Fakultets)
class FakultetsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Yonalishs)
class YonalishsAdmin(admin.ModelAdmin):
    list_display = ['id', 'fakultet', 'name']
    search_fields = ['name']
    ordering = ['fakultet', 'name']

@admin.register(Kurs)
class KursAdmin(admin.ModelAdmin):
    list_display = ['id', 'yonalish', 'name']
    search_fields = ['name']
    ordering = ['yonalish', 'name']

@admin.register(Guruhs)
class GuruhsAdmin(admin.ModelAdmin):
    list_display = ['id', 'kurs', 'name']
    search_fields = ['name']
    ordering = ['kurs', 'name']
