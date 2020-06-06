"""Server Side FCM sample.
Firebase Cloud Messaging (FCM) can be used to send messages to clients on iOS,
Android and Web.
This sample uses FCM to send two types of messages to clients that are subscribed
to the `news` topic. One type of message is a simple notification message (display message).
The other is a notification message (display notification) with platform specific
customizations. For example, a badge is added to messages that are sent to iOS devices.
"""

import argparse
import json
import requests

from oauth2client.service_account import ServiceAccountCredentials
'''
firebase: {
    apiKey: "AIzaSyD8HDPcKRluB3EpxHbhEUCTkkdB1F-xz30",
    authDomain: "breakit-aeb3c.firebaseapp.com",
    databaseURL: "https://breakit-aeb3c.firebaseio.com",
    projectId: "breakit-aeb3c",
    storageBucket: "breakit-aeb3c.appspot.com",
    messagingSenderId: "460842117127",
    appId: "1:460842117127:web:c5c504ad65564cffb1a2a2",
    measurementId: "G-F6L1R0M4KH"
  }
'''
PROJECT_ID = 'breakit-aeb3c'
BASE_URL = 'https://fcm.googleapis.com'
FCM_ENDPOINT = 'v1/projects/' + PROJECT_ID + '/messages:send'
FCM_URL = BASE_URL + '/' + FCM_ENDPOINT
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

# [START retrieve_access_token]
def _get_access_token():
	"""Retrieve a valid access token that can be used to authorize requests.
	:return: Access token.
	"""
	credentials = ServiceAccountCredentials.from_json_keyfile_name('service-accounts.json', SCOPES)
	access_token_info = credentials.get_access_token()
	return access_token_info.access_token
	# [END retrieve_access_token]

def _send_fcm_message(fcm_message):
	"""Send HTTP request to FCM with given message.
	Args:
	fcm_message: JSON object that will make up the body of the request.
	"""
	# [START use_access_token]
	headers = {
		'Authorization': 'Bearer ' + _get_access_token(),
		'Content-Type': 'application/json; UTF-8',
	}
	# [END use_access_token]
	resp = requests.post(FCM_URL, data=json.dumps(fcm_message), headers=headers)

	if resp.status_code == 200:
		print('Message sent to Firebase for delivery, response:')
		print(resp.text)
		print(resp)
		return True
	else:
		print('Unable to send message to Firebase')
		print(resp.text)
		return False

def _build_common_message(token, notification=None, validate_only=False):
	"""Construct common notifiation message.
	Construct a JSON object that will be used to define the
	common parts of a notification message that will be sent
	to any app instance subscribed to the news topic.
	"""
	if notification is None:
		notification = {
			"body" : "Ypour order is ready", 
			"title": "Ypour order is ready i m here"
		}

	data_payload = {
		"webpush" : {
			"notification": notification,
			"fcm_options": {
				"analytics_label": "breakit",
				"link": "https://anarchistmegabyte.github.io/breakit-app/home"
			}
		},
		"token": token
	}

	return {
		"validate_only": validate_only,
		"message": data_payload
	}


# fcm_message = _build_common_message(1, "doB4kEHRg-Y:APA91bEUncwFnR-e_fjlXhOTKlFdB7UB-NIEWjl3SmGcKF5MkjFsgEil20lXW8Mx-2l1Jc_vhZMrxUQSgbNld_GBl5vKTPTbuyRN_lP-svTu3c4bBW44ZtO_LHUu0t2ZeERveOVII2jG") 
# _send_fcm_message(fcm_message) 

def delete_invalid_tokens(user_id):
	from fcm_django.models import FCMDevice
	user_tokens = FCMDevice.objects.filter(user__id=user_id)#.values_list("registeration_id", flat=True)
	for each_device in user_tokens:
		print("##################################################") 
		mess = _build_common_message(1, each_device.registration_id, data=None, validate_only=True)
		print(mess)
		res = _send_fcm_message(mess) 
		print(res)
		if not res:
			#delete entry from fcm_django table
			each_device.delete()
