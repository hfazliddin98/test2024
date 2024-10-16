from django.contrib import admin
from users.models import Talaba

@admin.register(Talaba)
class TalabaAdmin(admin.ModelAdmin):
    list_display = ['tast_id']
