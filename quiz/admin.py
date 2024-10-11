from django.contrib import admin
from quiz.models import Mavzular, Testlar

 
@admin.register(Testlar)
class TestlarAdmin(admin.ModelAdmin):
    list_display = ['id', 'mavzu_id', 'savol']
    search_fields = ['savol']


@admin.register(Mavzular)
class MavzularAdmin(admin.ModelAdmin):
    list_display = ['id', 'mavzu']
    search_fields = ['mavzu']


admin.site.register([])