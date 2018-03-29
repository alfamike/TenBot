# This Python file uses the following encoding: utf-8
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

@bot.message_handler(commands=['stats'], content_types=['text'])
def stats_handler(message):
    f= open('../tmp/prueba.html','w')
    pagina= '''<!DOCTYPE HTML><html><head><title>Resultados</title></head><body><h1>
    Hola mundo</h1><p>Cuerpo</p></body></html>'''
    f.write(pagina)
    f.close()

    f= open('../tmp/prueba.html','r')
    cid= message.chat.id
    bot.send_document(cid,f)

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)
bot.polling()