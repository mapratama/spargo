from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    search_fields = ('name', )
    ordering = ('name',)
