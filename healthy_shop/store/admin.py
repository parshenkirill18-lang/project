from django.contrib import admin
from .models import Product, Category

# Сначала снимаем старую регистрацию Product, если она есть
try:
    admin.site.unregister(Product)
except admin.sites.NotRegistered:
    pass

# Настраиваем отображение продукта в админке
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'weight', 'quantity_per_package')
    list_filter = ('category',)
    search_fields = ('name',)

# Регистрируем Product с новой настройкой
admin.site.register(Product, ProductAdmin)

# Регистрируем категории
admin.site.register(Category)
