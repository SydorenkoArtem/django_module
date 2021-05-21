from django.contrib import admin

from product.models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ["category", "product", "amount", "price", "description", "pic"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ["category"]
