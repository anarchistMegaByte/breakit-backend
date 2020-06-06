from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from foodmenu.models import MenuForTheDay
from datetime import datetime, date, timedelta
from breakit.settings import MEDIA_URL, MEDIA_ROOT


# Create your views here.
@require_http_methods(["GET"])
@csrf_exempt
def get_todays_menu(request):
    all_menu = MenuForTheDay.objects.filter(date=date.today() + timedelta(days=1))
    result_dict = []
    print(MEDIA_ROOT + MEDIA_URL)
    for each_m in all_menu:
        menu = {}
        menu["menu_of_the_day_id"] = each_m.id
        menu["food_item_id"] = each_m.fooditem_fk.id
        menu["image"] = "https://fc425648a9d9.ngrok.io" + each_m.fooditem_fk.image.url
        menu["item"] = each_m.fooditem_fk.name
        menu["restaurant"] = each_m.fooditem_fk.restaurant_fk.name
        menu["price"] = each_m.fooditem_fk.price
        menu["is_veg"] = each_m.fooditem_fk.is_veg
        result_dict.append(menu)
    print(result_dict)
    return JsonResponse({"data": result_dict})