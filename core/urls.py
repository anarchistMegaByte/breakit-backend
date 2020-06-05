from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^v1/register_or_login_otp/$', views.register_or_login_otp, name="register_or_login_otp"),
    url(r'^v1/verify_otp/$', views.verify_otp, name="verify_otp"),
    url(r'^v1/create_or_update_user_pref/$', views.create_or_update_user_pref, name="create_or_update_user_pref"),
    url(r'^v1/confirm_order/$', views.confirm_order, name="confirm_order"),
    url(r'^v1/get_all_delivery_slots/$', views.get_all_delivery_slots, name="get_all_delivery_slots"),
    url(r'^v1/register_token/$', views.register_token, name="register_token"),
]