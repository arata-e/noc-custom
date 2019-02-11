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
            #pprint(utm.search_user('15500739'))
            services = utm.call('rpcf_get_all_services_for_user',{'account_id' : account_id})
            pprint(services)
            for i in range(len(services['slink_id_count'])):
                if services['slink_id_count'][i]['service_type_array'] == 3:
                    data = {'slink_id' : services['slink_id_count'][i]['slink_id_array']}
                    pprint(data)
                    service = utm.call('rpcf_get_iptraffic_service_link', data)
                    pprint(service)
        else:
            print("Need --account parametr")

if __name__ == "__main__":
    Command().run()
