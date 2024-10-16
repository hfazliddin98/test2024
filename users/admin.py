from django.contrib import admin
from users.models import Fakultets, Yonalishs, Kurs, Guruhs



@admin.register(Fakultets)
class FakultetsAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Yonalishs)
class YonalishsAdmin(admin.ModelAdmin):
    list_display = ['fakultet_id', 'name']

@admin.register(Kurs)
class KursAdmin(admin.ModelAdmin):
    list_display = ['yonalish_id', 'name']

@admin.register(Guruhs)
class GuruhsAdmin(admin.ModelAdmin):
    list_display = ['kurs_id', 'name']
