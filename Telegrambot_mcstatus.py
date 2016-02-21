from mcstatus import MinecraftServer
from telegram import Updater
import logging

token="TOKEN"
updater = Updater(token)
dispatcher = updater.dispatcher

#Enable logging
logging.basicConfig(
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",level=logging.INFO)
logger = logging.getLogger()

def start(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="I'll tell you the status of a Minecraft Server if you ask with \n /online address")
dispatcher.addTelegramCommandHandler("start", start)

def help(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="I'll tell you the status of a Minecraft Server if you ask with \n /online address")
dispatcher.addTelegramCommandHandler("help", help)

def online(bot, update, args):
	try:
		chat_id = update.message.chat_id
		address = args[0]
		server = MinecraftServer(address)
		status = server.status()
		bot.sendMessage(chat_id=chat_id, text=("{0} ({1}) v{2} {3}ms Players online {4}/{5}".format(status.description, address, status.version.name, status.latency, status.players.online,status.players.max)))
	except IndexError:
		bot.sendMessage(chat_id=chat_id, text="I need the adress you want me to lookup\n Try with /online Adress ")
dispatcher.addTelegramCommandHandler("online", online)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))
dispatcher.addErrorHandler(error)

updater.start_polling()