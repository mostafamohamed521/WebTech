from django.contrib import admin
from .models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "label", "city", "country", "is_default")
    list_filter = ("country", "is_default")
    search_fields = ("user__email", "city", "street")
