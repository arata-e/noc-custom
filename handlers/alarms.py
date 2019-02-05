import json
import os
import sys
import syslog
import requests
from pprint import pprint
import apiai

def aievent(alarm):
#    logging.info(json.dumps(dir(alarm)))
#    syslog.openlog(acility=syslog.LOCAL2)
#    syslog.syslog(syslog.LOG_INFO, json.dumps(alarm.body))
    request = apiai.ApiAI('19dcd04dff844d089496a3e1b0a32e95').text_request()
    request.lang = 'en'
    request.session_id = 'RNNOCAlarmAI'
    request.query = json.dumps(alarm.body)
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
#    syslog.syslog(syslog.LOG_INFO, json.dumps(responseJson))
    


