from django.contrib import admin
from .models import Item, Cart, Cart_Item, Payment_Info
# Register your models here.
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(Cart_Item)
admin.site.register(Payment_Info)

