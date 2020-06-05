from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from core.models import User, UserProfile, OrderDetails, OrderItems
from foodmenu.models import FoodItems
from breakit.settings import DEFAULT_RESPONSE_AS_DICT, SMS_API_KEY
from utilities.sms import sendSMS
import random
import redis
from datetime import date
import time
import traceback

# Create your views here.
@require_http_methods(["POST"])
@csrf_exempt
def register_or_login_otp(request):
    result_dict = DEFAULT_RESPONSE_AS_DICT.copy()
    data = json.loads(request.body.decode('utf-8'))
    phone_number = data["phone_number"]
    
    try:
        user, created  = User.objects.get_or_create(phone_number=phone_number)
    except Exception as e:
        result_dict["messgae"] = str(e)

    # generate otp
    r = redis.Redis(host='localhost', port=6379, db=0)
    otp = r.get(str(user.phone_number))
    if otp is None:
        otp = random.randint(1000,9999)
    r.set(str(user.phone_number), str(otp), ex=60)

    resp =  sendSMS(str(user.phone_number)[-10:], "Your OTP for breakIt login is " + str(otp))
    resp = json.loads(resp)
    if resp["status"] == "failure":
        result_dict["messgae"] = "SMS provider seems to be down please try again in some time."
        print(str(user.phone_number))
        r.set(str(user.phone_number), "1234", ex=60)
    else:
        result_dict["message"] = "OTP sent successfully."
        result_dict["status"] = True
    return JsonResponse(result_dict)


@require_http_methods(["POST"])
@csrf_exempt
def verify_otp(request):
    result_dict = DEFAULT_RESPONSE_AS_DICT.copy()
    data = json.loads(request.body.decode('utf-8'))
    phone_number = data["phone_number"]
    otp = data["otp"]

    r = redis.Redis(host='localhost', port=6379, db=0)
    rotp = r.get(phone_number)
    if rotp is not None:
        if int(rotp) == int(otp):
            up = UserProfile.objects.get(user_fk__phone_number=phone_number)
            data_return = {}
            data_return["user_id"] = up.user_fk.id
            data_return["address"] = up.address
            data_return["delivery_slot"] = up.delivery_slot_pref
            data_return["pincode"] = up.pincode
            result_dict["data"] = data_return
            result_dict["message"] = "OTP registeration successfull."
            result_dict["status"] = True
        else:
            result_dict["message"] = "OTP not matched."    
    else:
        result_dict["message"] = "OTP not found." 
    return JsonResponse(result_dict)


@require_http_methods(["POST"])
@csrf_exempt
def create_or_update_user_pref(request):
    result_dict = DEFAULT_RESPONSE_AS_DICT.copy()
    data = json.loads(request.body.decode('utf-8'))
    try:
        phone_number = data["phone_number"]
        address = data["address"]
        pincode = int(data["pincode"])
        delivery_slot = data["delivery_slot"]

        from core.request_helpers import create_or_update_user_profile
        up = create_or_update_user_profile(phone_number, address, pincode, delivery_slot)
        
        result_dict["message"] = "User Profile Created Successfully."
        result_dict["status"] = True
        data_return = {}
        data_return["user_id"] = up.user_fk.id
        data_return["address"] = up.address
        data_return["delivery_slot"] = up.delivery_slot_pref
        data_return["pincode"] = up.pincode
        result_dict["data"] = data_return
    except Exception as e:
        traceback.print_exc()
        result_dict["message"] = str(e)
    
    return JsonResponse(result_dict)


@require_http_methods(["POST"])
@csrf_exempt
def confirm_order(request):
    result_dict = DEFAULT_RESPONSE_AS_DICT.copy()
    data = json.loads(request.body.decode('utf-8'))
    try:
        phone_number = data["phone_number"]
        address = data["address"]
        pincode = int(data["pincode"])
        delivery_slot = data["delivery_slot"]
        #[{"menu_id": id, "qty":5}]
        menu_items = data["menu_items"]

        from core.request_helpers import create_or_update_user_profile
        up = create_or_update_user_profile(phone_number, address, pincode, delivery_slot)
        
        od = OrderDetails()
        od.order_id = int(time.time()*1000)
        od.order_date = date.today()
        od.user_fk = up.user_fk
        od.total_cost = data["total_cost"]
        od.save()

        cost = 0
        for each_item in menu_items:
            menu_item = FoodItems.objects.get(id = each_item["menu_id"])
            oi = OrderItems()
            oi.order_details_fk = od
            oi.menu_items_fk = menu_item
            oi.qty = each_item["qty"]
            oi.item_cost = menu_item.price * oi.qty
            cost = cost + oi.item_cost
            oi.save()

        od.total_cost = cost
        od.save()

        result_dict["message"] = "User Profile Created Successfully."
        result_dict["status"] = True
        data_return = {}
        data_return["user_id"] = up.user_fk.id
        data_return["address"] = up.address
        data_return["delivery_slot"] = up.delivery_slot
        data_return["pincode"] = up.pincode
        data_return["order_id"] = od.order_id
        data_return["total_cost"] = od.total_cost
        data_return["order_date"] = od.order_date
        result_dict["data"] = data_return
    except Exception as e:
        result_dict["message"] = str(e)
    
    return JsonResponse(result_dict)


@require_http_methods(["GET"])
@csrf_exempt
def get_all_delivery_slots(request):
    result_dict = []
    for each_slot in UserProfile.SLOT_CHOICES:
        result_dict.append(each_slot[1])
    print(result_dict)
    return JsonResponse({"data": result_dict})