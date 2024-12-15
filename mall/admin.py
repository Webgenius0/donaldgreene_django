from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Category, Product, ColorVariant, SizeVariant


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    pass 

@admin.register(ColorVariant)
class ColorVariantAdmin(ModelAdmin):
    pass 

@admin.register(SizeVariant)
class ColorVariantAdmin(ModelAdmin):
    pass 

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'price', 'category','created_at')
    list_filter = ('category', 'color_variant', 'size_variant')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)