# coding: utf-8
import requests
from requests.auth import HTTPDigestAuth
import json
from pprint import pprint
import argparse
from utm5 import UTM5
from noc.core.management.base import BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-a", "--account", dest="account", default=None)

    def handle(self, *args, **options):
        account_id = options.get("account")
        if account_id:
            logins = []
            utm = UTM5()
            services = utm.get_slinks_for_account(account_id)
            if services['Result'] == 'Ok':
                for i in range(len(services['data'])):
                    if services['data'][i]['service_type_array'] == 3:
                        service = utm.get_ipslink_data(services['data'][i]['slink_id_array'])
                        if 'iptraffic_login' in service['data']:
                            if service['data']['iptraffic_login'] != '':
                                logins.append(service['data']['iptraffic_login'])
                    if services['data'][i]['service_type_array'] == 5:
                        service = utm.get_dhsslink_data(services['data'][i]['slink_id_array'])
                        if 'login' in service['data']:
                            if service['data']['login'] != '':
                                logins.append(service['data']['login'])
                if len((logins)) > 0:
                    from noc.sa.models.action import Action
                    from noc.sa.models.managedobject import ManagedObject
                    action = Action.objects.get(name='clearsession')
                    bras = [ManagedObject.objects.get(id=105), ManagedObject.objects.get(id=86)]
                    commands = [[str(action.expand(mo,username=x))] for x in logins]
                    pprint(commands)
                    #[bras[0].mo.scripts.commands(commands=[]

        else:
            print("Need --account parametr")

if __name__ == "__main__":
    Command().run()
