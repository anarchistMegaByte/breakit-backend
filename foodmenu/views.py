from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from foodmenu.models import MenuForTheDay
from datetime import datetime, date, timedelta


# Create your views here.
@require_http_methods(["GET"])
@csrf_exempt
def get_todays_menu(request):
    all_menu = MenuForTheDay.objects.filter(date=date.today() + timedelta(days=1))
    result_dict = []
    for each_m in all_menu:
        menu = {}
        menu["menu_of_the_day_id"] = each_m.id
        menu["food_item_id"] = each_m.fooditem_fk.id
        menu["image"] = each_m.fooditem_fk.image.url
        menu["item"] = each_m.fooditem_fk.name
        menu["restaurant"] = each_m.fooditem_fk.restaurant_fk.name
        menu["price"] = each_m.fooditem_fk.price
        menu["is_veg"] = each_m.fooditem_fk.is_veg
        result_dict.append(menu)
    print(result_dict)
    return JsonResponse({"data": result_dict})