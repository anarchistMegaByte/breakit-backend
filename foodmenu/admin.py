from django.contrib import admin
from .models import Restaurants, FoodItems, MenuForTheDay

# Register your models here.
class RestaurantsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Restaurants._meta.get_fields() if field.auto_created == False]


class FoodItemsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FoodItems._meta.get_fields() if field.auto_created == False]


class MenuForTheDayAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MenuForTheDay._meta.get_fields() if field.auto_created == False]


admin.site.register(Restaurants, RestaurantsAdmin)
admin.site.register(FoodItems, FoodItemsAdmin)
admin.site.register(MenuForTheDay, MenuForTheDayAdmin)
