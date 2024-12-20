from django.contrib import admin
from .models import Client, Employee, Product, Order, OrderDetails

class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'address', 'phone', 'email')
    search_fields = ('first_name', 'last_name', 'email')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'position', 'salary', 'hire_date')
    search_fields = ('first_name', 'last_name', 'position')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'price')
    search_fields = ('name', 'type')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_date', 'total_price', 'status', 'get_client_name', 'get_employee_name')
    search_fields = ('status',)
    list_filter = ('status', 'order_date')

    def get_client_name(self, obj):
        return f"{obj.client.first_name} {obj.client.last_name}"
    get_client_name.short_description = 'Client'

    def get_employee_name(self, obj):
        return f"{obj.employee.first_name} {obj.employee.last_name}"
    get_employee_name.short_description = 'Employee'

class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_order_id', 'get_product_name', 'quantity')
    search_fields = ('order__id', 'product__name')

    def get_order_id(self, obj):
        return obj.order.id
    get_order_id.short_description = 'Order ID'

    def get_product_name(self, obj):
        return obj.product.name
    get_product_name.short_description = 'Product'

admin.site.register(Client, ClientAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetails, OrderDetailsAdmin)
