from django.contrib import admin
from .models import Category, MenuItem, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'available')
    list_filter = ('category',)
    search_fields = ('name',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'created_at', 'status', 'total_price')
    inlines = [OrderItemInline]
    list_filter = ('status',)

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Order, OrderAdmin)