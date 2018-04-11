# This Python file uses the following encoding: utf-8
'''
Created on 28 mar. 2018

@author: Alvaro
'''
import telebot
import pysnmp
import pysmi
from pysnmp.hlapi import *
from telebot.types import *
from telebot.apihelper import *
from telebot.util import *
from pysnmp.smi.rfc1902 import *

TOKEN= "583704103:AAEiWiGV2XxMzRNDJGiJ2FSseR4InXB_un8"
bot= telebot.TeleBot(TOKEN)
motor_snmp= SnmpEngine()
comunidad= CommunityData('grupo10')
target_agente=UdpTransportTarget(('10.10.10.1', 161))
#comunidad= CommunityData('public')
#target_agente=UdpTransportTarget(('demo.snmplabs.com', 161))

@bot.message_handler(commands=['start'])
def start_handler(message):
    cid= message.chat.id
    start_message= '''Bienvenido al bot de Gestión del Grupo 10\nUtilice el comando /help para ver las opciones
disponibles.'''
    bot.send_message(cid, start_message)
    
@bot.message_handler(commands=['help'])
def help_handler(message):
    cid= message.chat.id
    help_message= '''Aquí tiene los comandos implementados para la gestión del switch HP-ProCurve:\n/system get - Devuelve la localización, el nombre, el tiempo en marcha y la persona de contacto del sistema.\n/system set - Configura la localización, el nombre y la persona de contacto del sistema.\n/system set localizacion <localizacion>\n/system set nombre <nombre>\n/system set contacto <contacto>\n/fdb - Devuelve la forwarding database\n'''
    bot.send_message(cid, help_message)

@bot.message_handler(commands=['system'])
def system_handler(message):
    cid= message.chat.id
    parametros= message.text.split()
    try: 
        if parametros[1]== 'get':
            location= next(getCmd(motor_snmp, comunidad,target_agente,ContextData(),
                         ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0))))
            location_string=str(location[3][0]).split('=')
            coordenadas= location_string[1].split()
            latitude= coordenadas[0]
            longitude= coordenadas[1]
            location_answer= 'sysLocation: '+ location_string[1]
            bot.send_location(cid, latitude, longitude)
            bot.send_message(cid, location_answer)
            
            nombre_sistema= next(getCmd(motor_snmp, comunidad,target_agente,ContextData(),
                         ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0))))
            nombre_sistema_string= str(nombre_sistema[3][0]).split('=')
            nombre_sistema_answer= 'sysName: '+ str(nombre_sistema_string[1])
            bot.send_message(cid, nombre_sistema_answer)
            
            tiempo_sistema= next(getCmd(motor_snmp, comunidad,target_agente,ContextData(),
                         ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0))))
            tiempo_sistema_string= str(tiempo_sistema[3][0]).split('=')
            tiempo_sistema_answer= 'sysUpTime: '+ str(tiempo_sistema_string[1])
            bot.send_message(cid, tiempo_sistema_answer)
            
            contacto_sistema= next(getCmd(motor_snmp, comunidad,target_agente,ContextData(),
                         ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysContact', 0))))
            contacto_sistema_string= str(contacto_sistema[3][0]).split('=')
            contacto_sistema_answer= 'sysContact: '+ str(contacto_sistema_string[1])
            bot.send_message(cid, contacto_sistema_answer)
            
        elif parametros[1]== 'set':
            if  parametros[2]== 'localizacion':
                location= next(setCmd(motor_snmp, comunidad,target_agente,ContextData(),
                         ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0), parametros[3])))
                location_string=str(location[3][0]).split('=')
                coordenadas= location_string[1].split()
                latitude= coordenadas[0]
                longitude= coordenadas[1]
                location_answer= 'sysLocation ha sido modificado con éxito: '+ location_string[1]
                bot.send_message(cid, location_answer)
                
            if  parametros[2]== 'nombre':
                nombre_sistema= next(setCmd(motor_snmp, comunidad,target_agente,ContextData(),
                         ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0), parametros[3])))
                nombre_sistema_string= str(nombre_sistema[3][0]).split('=')
                nombre_sistema_answer= 'sysName ha sido modificado con éxito: '+ str(nombre_sistema_string[1])
                bot.send_message(cid, nombre_sistema_answer)
                
            if  parametros[2]== 'contacto':
                contacto_sistema= next(setCmd(motor_snmp, comunidad,target_agente,ContextData(),
                         ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysContact', 0), parametros[3])))
                contacto_sistema_string= str(contacto_sistema[3][0]).split('=')
                contacto_sistema_answer= 'sysContact: '+ str(contacto_sistema_string[1])
                contacto_sistema_answer= 'sysContact ha sido modificado con éxito: '+ str(contacto_sistema_string[1])
                bot.send_message(cid, contacto_sistema_answer)
        else:
            bot.send_message(cid, 'Comando no reconocido. Consulte /help') 
    except(IndexError):
        bot.send_message(cid, 'Comando incompleto. Consulte /help')
        
        
        
@bot.message_handler(commands=['fdb'], content_types=['text'])
def fdb_handler(message):
    fdbTable= next(bulkCmd(motor_snmp, comunidad, target_agente, ContextData(), 0, 28,
                            ObjectType(ObjectIdentity('BRIDGE-MIB','dot1dTpFdbAddress')), 
                             ObjectType(ObjectIdentity('BRIDGE-MIB','dot1dTpFdbPort')),
                             ObjectType(ObjectIdentity('BRIDGE-MIB','dot1dTpFdbStatus'))))
    answer= fdbTable[3]
    primeraFila= [str(answer[0][1]), answer[0][2], answer[0][3]]
    segundaFila= [str(answer[1][1]), answer[1][2], answer[1][3]]
    terceraFila= [str(answer[2][1]), answer[2][2], answer[2][3]]
    tablaStr= str(primeraFila)+','+str(segundaFila)+','+str(terceraFila)
    
    f= open('../tmp/fdb.html','w')
    pagina= '''<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['table']});
      google.charts.setOnLoadCallback(drawTable);

      function drawTable() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'dot1dTpFdbAddress');
        data.addColumn('number', 'dot1dTpFdbPort');
        data.addColumn('number', 'dot1dTpFdbStatus');
        data.addRows(['''+tablaStr+'''
        ]);

        var table = new google.visualization.Table(document.getElementById('table_div'));

        table.draw(data, {showRowNumber: false, width: '100%', height: '100%'});
      }
    </script>
  </head>
  <body>
    <div id="table_div"></div>
  </body>
</html>'''
    f.write(pagina)
    f.close()
    f= open('../tmp/fdb.html','r')
    cid= message.chat.id
    bot.send_document(cid,f)
    
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
    
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)
bot.polling()