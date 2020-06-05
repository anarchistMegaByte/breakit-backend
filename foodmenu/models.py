from django.db import models

# Create your models here.
class Restaurants(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False, unique=True)
    address = models.TextField(blank=True, null=True, default=None)
    pincode = models.IntegerField(blank=False, null=False)
    
    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = "Restaurants"

    def __str__(self):
        return str(self.name)


class FoodItems(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False, unique=True)
    description = models.TextField(blank=True, null=True, default=None)
    restaurant_fk = models.ForeignKey(Restaurants, on_delete=models.CASCADE, related_name="restaurants")
    price = models.IntegerField(blank=False, null=False)
    image = models.ImageField(upload_to='menuitems')
    is_veg = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Food Item'
        verbose_name_plural = "Food Items"

    def __str__(self):
        return str(self.name)


class MenuForTheDay(models.Model):
    date = models.DateField(blank=False, null=False)
    fooditem_fk = models.ForeignKey(FoodItems, on_delete=models.CASCADE, related_name="restaurants")

    class Meta:
        verbose_name = 'Menu For The Day'
        verbose_name_plural = "Menu For The Day"

    def __str__(self):
        return str(self.fooditem_fk) + "-" + str(self.fooditem_fk.restaurant_fk.name)