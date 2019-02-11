import requests
from requests.auth import HTTPDigestAuth
import json
from pprint import pprint
#NOC modules
from noc.main.models.remotesystem import RemoteSystem, EnvItem

url = "http://addusertest.ccs.ru:82/api/v1/"
headers = {'Content-type': 'application/json'}

class UTM5:

    def __init__(self):
        self.remote_system = RemoteSystem.objects.get(name = 'UTM5')
        self.apikey = self.remote_system.config['apikey']
        self.apiurl = self.remote_system.config['apiurl']

    def call(self, function='', data = None):
        r = self.apiurl+"utm5/call/" + function + '?apiKey=' + self.apikey
        if data:
            response = requests.put(r,verify=True, json=data, headers=headers)
        else:
            response = requests.put(r,verify=True,  headers=headers)
        if (response.ok):
            return json.loads(response.content)
        else:
            response.raise_for_status()

    def search_user(self, username = ''):
        result = {"Result" : "Not found"}
        whatid = 2;
        what   = username;
        data   = {
                'poles_count' : {
                    0 : {
                        'pole_code_array' : 44
                        }
                    },
                'select_type' : 0,
                'patterns_count' : {
                0 : {
                    'what' : whatid,
                    'criteria_id' : 3,
                    'pattern' : what
                    }
                }
            }
        #    return $data;
        res    = self.call('rpcf_search_users_new', data);
        size   = len(res['user_data_size']);
        if (size != 0):
            result   = {
                "Result" : "Ok",
                "data" : {}
                }
            result['data'] = res['user_data_size'][0];
        
        return result;

    def get_user_id(self, username = ''):
        result = {"Result" : "Not found"}
        whatid = 2;
        what   = username;
        data   = {
                'poles_count' : {
                    0 : {
                        'pole_code_array' : 44
                        }
                    },
                'select_type' : 0,
                'patterns_count' : {
                0 : {
                    'what' : whatid,
                    'criteria_id' : 3,
                    'pattern' : what
                    }
                }
            }
        #    return $data;
        res    = self.call('rpcf_search_users_new', data);
        size   = len(res['user_data_size']);
        if (size != 0):
            result   = {
                "Result" : "Ok",
                "data" : {}
                }
            result['data'] = { 'user_id' : res['user_data_size'][0]['user_id']};
        
        return result;


    def get_user_info(self, username = ''):
        result = {"Result" : "Not found"}
        user_id = self.get_user_id(username)
        if user_id['Result'] != 'Ok':
            user_id = temp['data']['user_id']
        res    = self.call('rpcf_get_userinfo', user_id['data']);
        size   = len(res);
        if (size != 0):
            result   = {
                "Result" : "Ok",
                "data" : {}
                }
            result['data'] = res;
        
        return result;


