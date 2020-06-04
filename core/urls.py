from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^v1/create_user/$', views.create_user, name="create_user"),
]