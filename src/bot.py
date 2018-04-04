# This Python file uses the following encoding: utf-8
'''
Created on 28 mar. 2018

@author: Alvaro
'''
import telebot
import pysnmp
from pysnmp.hlapi import *
from telebot.types import *
from telebot.apihelper import *
from telebot.util import *
from pysnmp.proto.rfc1902 import *
from pysnmp.smi.rfc1902 import *

TOKEN= "583704103:AAEiWiGV2XxMzRNDJGiJ2FSseR4InXB_un8"
bot= telebot.TeleBot(TOKEN)
motor_snmp= SnmpEngine()
comunidad= CommunityData('grupo10')
target_agente=UdpTransportTarget(('10.10.10.1', 161))

@bot.message_handler(commands=['start'])
def start_handler(message):
    cid= message.chat.id
    start_message= '''Bienvenido al bot de Gestión del Grupo 10\nUtilice el comando /help para ver las opciones
disponibles.'''
    bot.send_message(cid, start_message)
    
@bot.message_handler(commands=['help'])
def help_handler(message):
    cid= message.chat.id
    help_message= '''Aquí tiene los comandos implementados para la gestión del switch HP-ProCurve:\n'''
    bot.send_message(cid, help_message)

@bot.message_handler(commands=['system'])
def system_handler(message):
    cid= message.chat.id
    parametros= message.text.split()
    
    if parametros[1]== 'get':
        bot.send_location(cid, latitude=37.411604, longitude=-6.001790)
        location= next(getCmd(motor_snmp, comunidad,target_agente,ContextData(),
                     ObjectType(ObjectIdentity('RFC1213-MIB', 'sysLocation', 0)).addAsn1MibSource('http://mibs.snmplabs.com/asn1/RFC1213-MIB')))
        location_answer= str(location[3][1])
        bot.send_message(cid, location_answer)
        
        nombre_sistema= next(getCmd(motor_snmp, comunidad,target_agente,ContextData(),
                     ObjectType(ObjectIdentity('RFC1213-MIB', 'sysName', 0)).addAsn1MibSource('http://mibs.snmplabs.com/asn1/RFC1213-MIB')))
        nombre_sistema_answer= str(nombre_sistema[3][1])
        bot.send_message(cid, nombre_sistema_answer)
        
        tiempo_sistema= next(getCmd(motor_snmp, comunidad,target_agente,ContextData(),
                     ObjectType(ObjectIdentity('RFC1213-MIB', 'sysUpTime', 0)).addAsn1MibSource('http://mibs.snmplabs.com/asn1/RFC1213-MIB')))
        tiempo_sistema_answer= str(tiempo_sistema[3][1])
        bot.send_message(cid, tiempo_sistema_answer)
    elif parametros[1]== 'set':
       dfs 
    else:
        bot.send_message(cid, 'Comando no reconocido. Consulte /help') 
        
@bot.message_handler(commands=['stats'], content_types=['text'])
def stats_handler(message):
    f= open('../tmp/prueba.html','w')
    pagina= '''<!DOCTYPE HTML><html>
  <head>
    <!--Load the AJAX API-->
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">

      // Load the Visualization API and the corechart package.
      google.charts.load('current', {'packages':['corechart']});

      // Set a callback to run when the Google Visualization API is loaded.
      google.charts.setOnLoadCallback(drawChart);

      // Callback that creates and populates a data table,
      // instantiates the pie chart, passes in the data and
      // draws it.
      function drawChart() {

        // Create the data table.
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Topping');
        data.addColumn('number', 'Slices');
        data.addRows([
          ['Mushrooms', 3],
          ['Onions', 1],
          ['Olives', 1],
          ['Zucchini', 1],
          ['Pepperoni', 2]
        ]);

        // Set chart options
        var options = {'title':'How Much Pizza I Ate Last Night',
                       'width':400,
                       'height':300};

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>

  <body>
    <!--Div that will hold the pie chart-->
    <div id="chart_div"></div>
  </body>
</html>'''
    f.write(pagina)
    f.close()

    f= open('../tmp/prueba.html','r')
    cid= message.chat.id
    bot.send_document(cid,f)
    #nombre_archivo='file:///C:/Users/Alvaro/OneDrive - UNIVERSIDAD DE SEVILLA/Universidad/Gestión_de_Redes/Proyecto/TenBot/tmp/prueba.html'
    #webbrowser.open_new(nombre_archivo)
    
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)
bot.polling()