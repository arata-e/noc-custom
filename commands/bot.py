import json
import os
import sys
import requests
import pyping
from pprint import pprint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# NOC modules
from noc.core.service.ui import UIService
from noc.sa.models.managedobject import ManagedObject
from noc.main.models.customfieldenumgroup import CustomFieldEnumGroup
from noc.main.models.customfieldenumvalue import CustomFieldEnumValue

class BotApplication(UIService):
    def startCommand(self,bot, update):
        chat_id = update.message.chat_id
        if chat_id in validuser:
             bot.send_message(chat_id=update.message.chat_id, text='?????')
        else:
            bot.sendMessage(chat_id=chat_id, text='Sorry, private area')
        
    def textMessage(self,bot, update):
        response = '' + update.message.text
        bot.send_message(chat_id=update.message.chat_id, text=response)

    def ping(self, bot, update, args):
         if not update.message.chat_id in validuser:
            return
         host = args[0]
         r = pyping.ping(host)
         if r.ret_code == 0:
             msg = ("{} Success".format(host))
         else:
             msg = "{} Failed with {}".format(host,r.ret_code)
         bot.send_message(chat_id=update.message.chat_id, text=msg)

    def start(self):
        updater = Updater(token=botkey)
        dispatcher = updater.dispatcher
        start_command_handler = CommandHandler('start', self.startCommand)
#        text_message_handler = MessageHandler(Filters.text, self.textMessage)
        dispatcher.add_handler(start_command_handler)
        ping_handler = CommandHandler('ping', self.ping, pass_args=True)
        dispatcher.add_handler(ping_handler)
#        dispatcher.add_handler(text_message_handler)
        updater.start_polling(clean=True)
        updater.idle()

    def api_data(self, req):
     try:
        data = json.loads(req.body.encode())
        return('{"message" : "I am heare"}')
        if 'channel_post' in data:
            message = str(data["channel_post"]["text"])
            chat_id = data["channel_post"]["chat"]["id"]
            first_name = data["channel_post"]["chat"]["title"]
            print(first_name)
        else:
            message = str(data["message"]["text"])
            chat_id = data["message"]["chat"]["id"]
            first_name = data["message"]["chat"]["first_name"]
            print("{}\n".format(first_name))

        if not any(chat_id == s for s in validuser):
            print(chat_id)
            print(' not valid user')
            return {"statusCode": 200}, None
        
        response = "Please /start, {}".format(first_name)

        if "start" in message:
            response = "Hello {}! Type /help to get list of actions.".format(first_name)

        if "help" in message:
            response = "/about - get information about rnnoc"

        if "about" in message:
            response = ("NOC bot for Raionet\n{}\t{}".format(chat_id,first_name))

        data = {"text": response.encode("utf8"), "chat_id": chat_id}
        url = BASE_URL + "/sendMessage"
        requests.post(url, data)

     except Exception as e:
        print(e)

     return {"statusCode": 200}, None

if __name__ == "__main__":
    BASE_URL = "https://api.telegram.org/bot{}".format('ACC_TELEGRAMRNNOCBOT_TOKEN')
    botkey = str(CustomFieldEnumValue.objects.get(key='botkey', enum_group=CustomFieldEnumGroup.objects.get(name='botkeys')).value)
    validuser=str(CustomFieldEnumValue.objects.get(key='validuser', enum_group=CustomFieldEnumGroup.objects.get(name='botkeys')).value).split(',')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    BotApplication().start()
