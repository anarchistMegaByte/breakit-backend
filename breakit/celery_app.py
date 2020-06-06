from __future__ import absolute_import, unicode_literals

import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'breakit.settings')

app = Celery('breakit')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
	print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
	'add-every-30-seconds': {
		'task': 'core.tasks.add',
		'schedule': 10.0
	},

	'everyday-nudge': {
		'task': 'core.tasks.everyday_nudge',
		'schedule': crontab(hour=14, minute=30)
	},

	# 'intellica-trip-info': {
	# 	'task': 'intellica.tasks.fetch_trip_data',
	# 	'schedule': crontab(minute=0, hour='*/3')
	# }
}

app.conf.timezone = 'UTC'
