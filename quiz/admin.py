from django.contrib import admin
from quiz.models import Mavzus, Tests, Natijas


 
@admin.register(Tests)
class TestsAdmin(admin.ModelAdmin):
    list_display = ['id', 'mavzu', 'savol', 'variant_a', 'variant_b', 'variant_c', 'variant_d', 'togri_javob']
    search_fields = ['savol', 'variant_a', 'variant_b', 'variant_c', 'variant_d']
    list_filter = ['mavzu']
    ordering = ['-id']


@admin.register(Mavzus)
class MavzusAdmin(admin.ModelAdmin):
    list_display = ['id', 'mavzu']
    search_fields = ['mavzu']
    ordering = ['mavzu']

@admin.register(Natijas)
class NatijasAdmin(admin.ModelAdmin):
    list_display = ['id', 'talaba', 'mavzu', 'fakultet', 'yonalish', 'kurs', 'guruh', 'togri', 'notogri', 'jami']
    search_fields = ['talaba']
    ordering = ['-id']

