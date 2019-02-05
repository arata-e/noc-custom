import json
import os
import sys
import requests
import pyping
from pprint import pprint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# NOC modules
from noc.core.service.ui import UIService
from noc.sa.models.managedobject import ManagedObject

BASE_URL = "https://api.telegram.org/bot{}".format('ACC_TELEGRAMRNNOCBOT_TOKEN')
validuser=[166518598, -1001264455094,736153621]

class BotApplication(UIService):
    def startCommand(self,bot, update):
        bot.send_message(chat_id=update.message.chat_id, text='?????')
        
    def textMessage(self,bot, update):
        pprint(dir(update))
        response = '' + update.message.text
        bot.send_message(chat_id=update.message.chat_id, text=response)

    def ping(self, bot, update, args):
         host = args[0]
         r = pyping.ping(host)

         if r.ret_code == 0:
             msg = ("Success")
         else:
             msg = "Failed with {}".format(r.ret_code)

         bot.send_message(chat_id=update.message.chat_id, text=msg)

    def start(self):
        updater = Updater(token='686384604:AAEbjmxrTHJP9ZlgQg53odgCML-egZZtI1g')
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
    BotApplication().start()
