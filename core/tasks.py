from celery import task
from datetime import datetime
import traceback
import time


@task()
def add():
	print("hello world...", datetime.now())
	pass

@task()
def everyday_nudge():
	from core.models import UserNotifToken
	from utilities.notificationPanel import _build_common_message, _send_fcm_message
	all_tokens = UserNotifToken.objects.all()
	for t in all_tokens:
		notification = {
			"body" : "Hello, BreakIt is Here.",
			"title": "Its time to order your breakfast for tommorrow."
		}
		_send_fcm_message(_build_common_message(t.token, notification=notification))
