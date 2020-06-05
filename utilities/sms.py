import urllib.request
import urllib.parse
from breakit.settings import SMS_API_KEY
 
def sendSMS(numbers, message):
    data =  urllib.parse.urlencode({'apikey': SMS_API_KEY, 'numbers': numbers,
        'message' : message})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)
 
# resp =  sendSMS('919320002501', 'This is your message')
# print (resp)