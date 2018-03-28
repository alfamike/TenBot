'''
Created on 28 mar. 2018

@author: Alvaro
'''
import telebot
import pysnmp

TOKEN= "583704103:AAEiWiGV2XxMzRNDJGiJ2FSseR4InXB_un8"
bot= telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message):
    cid= message.chat.id
    start_message= "Bienvenido al bot de Gestión del Grupo 10"
    bot.send_message(cid, start_message)

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()