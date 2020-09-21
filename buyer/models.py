from django.db import models
from django.conf import settings
import decimal
# Create your models here.
class Item(models.Model):
    def __str__(self):
        return self.item_text
    item_text = models.CharField(max_length=300)
    price =  models.DecimalField(decimal_places=2, max_digits=8)
    quantity = models.IntegerField()


class Cart_Item(models.Model):
    def __str__(self):
        return self.item_text
    item_text = models.CharField(max_length=300)
    price =  models.DecimalField(decimal_places=2, max_digits=8)
    quantity = models.IntegerField()

    def total_cart_item_price(self):
        return self.price * self.quantity

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=8)
    tax = models.DecimalField(decimal_places=2, max_digits=8)
    total_after_tax = models.DecimalField(decimal_places=2, max_digits=8)
    cart_items = models.ManyToManyField(Cart_Item)
    complete = models.BooleanField(default = False)

    def total_price(self):
        ans = 0
        for cart_item in self.cart_items.all():
            ans += cart_item.total_cart_item_price()
        return ans

class Payment_Info(models.Model):
        def __str__(self):
            return self.user
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
        price = models.DecimalField(decimal_places=2, max_digits=8)
        stripe_id = models.CharField(max_length=100)


