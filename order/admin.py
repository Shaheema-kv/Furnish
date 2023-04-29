from django.contrib import admin
from .models import Payment, Order, OrderProduct, Address
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','is_ordered')

admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Address)