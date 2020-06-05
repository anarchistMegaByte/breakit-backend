from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^v1/get_todays_menu/$', views.get_todays_menu, name="get_todays_menu"),
]