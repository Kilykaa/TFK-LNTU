from django.contrib import admin
from .models import Category, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category',
        'price',
        'manufacturer',
        'country',
        'product_type',
        'stock_status',
        'rating',
        'created_at'
    ]
    list_filter = [
        'category',
        'product_type',
        'stock_status',
        'country',
        'is_prescription_required',
        'rating',
        'created_at'
    ]
    search_fields = ['name', 'description', 'manufacturer']
    list_editable = ['price', 'stock_status', 'rating']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основна інформація', {
            'fields': ('name', 'category', 'description', 'product_type')
        }),
        ('Ціна та наявність', {
            'fields': ('price', 'stock_status', 'rating')
        }),
        ('Деталі товару', {
            'fields': ('manufacturer', 'country', 'dosage', 'package', 'is_prescription_required')
        }),
        ('Дати', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']

    def total_price(self, obj):
        if obj.pk:
            return f"{obj.total_price} грн"
        return "-"

    total_price.short_description = "Сума"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'customer_name',
        'customer_phone',
        'status',
        'total_amount',
        'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'customer_phone', 'customer_email']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Інформація про клієнта', {
            'fields': ('customer_name', 'customer_phone', 'customer_email', 'delivery_address')
        }),
        ('Замовлення', {
            'fields': ('status', 'total_amount', 'notes')
        }),
        ('Дати', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


admin.site.site_header = "Аптека Blin - Адміністрування"
admin.site.site_title = "Аптека Blin Admin"
admin.site.index_title = "Панель управління аптекою"