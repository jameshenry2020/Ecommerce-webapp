from django.contrib import admin
from product.models import Product,OrderProduct,Order,ShippingAddress,Payment

class OrderAdmin(admin.ModelAdmin):
    list_display=('user', 'ordered','being_delivered','received','shipping_address','payment')

    list_filter=['ordered',
                'being_delivered',
                'received',
                'shipping_address',
                'payment'
                ]
    list_display_links=[
                 'shipping_address',
                 'payment',
                  'user'
    ]
    search_fields=('user.username','ref_code')

class ProductAdmin(admin.ModelAdmin):
    list_display=('name','category','price')
    
# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderProduct)
admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingAddress)
admin.site.register(Payment)