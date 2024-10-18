from django.contrib import admin
from quiz.models import Mavzus, Tests, Talabas


 
@admin.register(Tests)
class TestsAdmin(admin.ModelAdmin):
    list_display = ['id', 'mavzu_id', 'savol', 'variant_a', 'variant_b', 'variant_c', 'variant_d']
    search_fields = ['savol']


@admin.register(Mavzus)
class MavzusAdmin(admin.ModelAdmin):
    list_display = ['id', 'mavzu']
    search_fields = ['mavzu']

