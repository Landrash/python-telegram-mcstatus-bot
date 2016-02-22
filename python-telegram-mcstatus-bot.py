#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""Telegram bot to check status of a specified Minecraft server

Commands:
/start Standard teĺegram bot start message. Same output as /help
/help Explains how to use the bot
/online Checks status of specified minecraft server. Use with /online ADDRESS"""

import logging
from mcstatus import MinecraftServer
from telegram import Updater

#Set token berore launching. Generate a token
TOKEN = "SETME"

helptext = "I'll tell you the status of a Minecraft Server if you ask with \n /online address"
onlinetext = "I need the adress you want me to lookup\n Try with /online ADDRESS"

#Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
    )
logger = logging.getLogger(__name__)

def bot_start(bot, update):
    """Standard telegram bot start message"""
    bot.sendMessage(chat_id=update.message.chat_id, text=helptext)

def bot_help(bot, update):
    """Explains how to use the bot"""
    bot.sendMessage(chat_id=update.message.chat_id, text=helptext)


def bot_online(bot, update, args):
    """Ónline function to check status of a Minecraft server"""
    try:
        chat_id = update.message.chat_id
        address = args[0]
        server = MinecraftServer(address)
        status = server.status()
        bot.sendMessage(
            chat_id=chat_id,
            text=("{0} ({1}) v{2} {3}ms Players online {4}/{5}".format(
                status.description,
                address,
                status.version.name,
                status.latency,
                status.players.online,
                status.players.max
            )))
    except IndexError:
        bot.sendMessage(chat_id=chat_id, text=onlinetext)
    except OSError:
        bot.sendMessage(chat_id=chat_id, text=onlinetext)

def bot_error(update, error):
    """Error handler"""
    logger.warning("Update %s caused error %s"(update, error))

def main():
    """Add command handlers specified earlier and start the bot."""
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.addTelegramCommandHandler("start", bot_start)
    dispatcher.addTelegramCommandHandler("online", bot_online)
    dispatcher.addTelegramCommandHandler("help", bot_help)
    dispatcher.addErrorHandler(bot_error)
    
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
