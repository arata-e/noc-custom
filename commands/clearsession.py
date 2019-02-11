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
            utm = UTM5()
            services = utm.get_slinks_for_account(account_id)
            pprint(services)
            if services['Result'] == 'Ok':
                for i in range(len(services['data'])):
                    if services['data'][i]['service_type_array'] == 3:
                        service = utm.get_ipslink_data(services['data'][i]['slink_id_array'])
                        pprint(service)
                    if services['data'][i]['service_type_array'] == 5:
                        service = utm.get_dhsslink_data(services['data'][i]['slink_id_array'])
                        pprint(service)
        else:
            print("Need --account parametr")

if __name__ == "__main__":
    Command().run()
