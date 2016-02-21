#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#Telegram bot to check status of a specified Minecraft server
#
#Commands
#/start Standard teĺegram bot start message. Same output as /help
#/help Explains how to use the bot
#/online Checks status of specified minecraft server. Use with /online ADDRESS

import logging
from mcstatus import MinecraftServer
from telegram import Updater

token="TOKEN" #Set token berore launching. Generate a token 
updater = Updater(token)
dispatcher = updater.dispatcher

#Enable logging
logging.basicConfig(
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
	,level=logging.INFO
	)
logger = logging.getLogger(__name__)

#Standard telegram bot start message
def start(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="I'll tell you the status of a Minecraft Server if you ask with \n /online address")

#Explains how to use the bot
def help(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="I'll tell you the status of a Minecraft Server if you ask with \n /online address")

#Ónline function to check status of a Minecraft server
def online(bot, update, args):
	try:
		chat_id = update.message.chat_id
		address = args[0]
		server = MinecraftServer(address)
		status = server.status()
		bot.sendMessage(chat_id=chat_id
			,text=("{0} ({1}) v{2} {3}ms Players online {4}/{5}".format(
				status.description
				, address
				, status.version.name
				, status.latency
				, status.players.online
				,status.players.max
				)))
	except IndexError:
		bot.sendMessage(chat_id=chat_id,text="I need the adress you want me to lookup\n Try with /online ADDRES")

#Error handler
def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

#Add command handlers specified earlier and start the bot. 
def main():
	dispatcher.addTelegramCommandHandler("start", start)
	dispatcher.addTelegramCommandHandler("online", online)
	dispatcher.addTelegramCommandHandler("help", help)
	dispatcher.addErrorHandler(error)
	
	updater.start_polling()
	updater.idle()

if __name__ == "__main__":
	main()