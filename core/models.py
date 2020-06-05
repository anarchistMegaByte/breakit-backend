from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.base_user import BaseUserManager
from foodmenu.models import FoodItems

# Create your models here.
class User(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ('username',)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = str(self.phone_number)

        if not self.password:
            self.set_unusable_password()

        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = "Users"

    def __str__(self):
        return str(self.phone_number)


class UserProfile(models.Model):
    slot_1 = "7:00 - 7:30 AM"
    slot_2 = "7:30 - 8:00 AM"
    slot_3 = "8:00 - 8:30 AM"
    slot_4 = "8:30 - 9:00 AM"
    slot_5 = "9:00 - 9:30 AM"
    slot_6 = "9:30 - 10:00 AM"

    SLOT_CHOICES = (
        (slot_1, slot_1),
        (slot_2, slot_2),
        (slot_3, slot_3),
        (slot_4, slot_4),
        (slot_5, slot_5),
        (slot_6, slot_6)
    )
    user_fk = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="profile")
    address = models.TextField(blank=False, null=False)
    pincode = models.IntegerField(blank=False, null=False)
    delivery_slot_pref = models.CharField(choices=SLOT_CHOICES, default=slot_1, max_length=250)

    class Meta:
        verbose_name = 'UserProfile'
        verbose_name_plural = "UserProfiles"

    def __str__(self):
        return str(self.user_fk) + "-" + str(self.delivery_slot_pref)


class OrderDetails(models.Model):
    order_id = models.BigIntegerField(blank=False, null=False)
    order_date = models.DateField(blank=False, null=False)
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total_cost = models.IntegerField(blank=False, null=False)
    sts = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'OrderDetail'
        verbose_name_plural = "OrderDetails"

    def __str__(self):
        return str(self.order_id) + "-" + str(self.user_fk) + "-" + str(self.user_fk.profile.delivery_slot_pref)


class OrderItems(models.Model):
    order_details_fk = models.ForeignKey(OrderDetails, on_delete=models.CASCADE, related_name="ordered_items")
    menu_items_fk = models.ForeignKey(FoodItems, on_delete=models.CASCADE, related_name="menu_item_in_order")
    qty = models.IntegerField(blank=False, null=False)
    item_cost = models.IntegerField(blank=False, null=False)

    class Meta:
        verbose_name = 'OrderItem'
        verbose_name_plural = "OrderItems"

    def __str__(self):
        return str(self.order_details_fk) + "-" + str(self.menu_items_fk) + "-" + str(self.qty)
