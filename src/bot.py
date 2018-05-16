# This Python file uses the following encoding: utf-8
'''
Created on 28 mar. 2018

@author: Alvaro
@version: 1.0
'''
import socketserver
import threading
import time

from pyasn1.codec.ber import decoder
import pysmi
import pysnmp
from pysnmp.hlapi import *
from pysnmp.proto import api
import pysnmp.proto.rfc1902
from pysnmp.smi.rfc1902 import *
import pysnmp.smi.rfc1902
import telebot
from telebot.apihelper import *
from telebot.types import *
from telebot.util import *


TOKEN= "583704103:AAEiWiGV2XxMzRNDJGiJ2FSseR4InXB_un8"
bot= telebot.TeleBot(TOKEN)
motor_snmp= SnmpEngine()
comunidad= CommunityData('grupo10')
target_agente=UdpTransportTarget(('10.10.10.1', 161))

#ACL
autorizados=[489720960,558338643]

@bot.message_handler(commands=['start'])
def start_handler(message):
    usuario= message.from_user
    chat_id= -172569293
    nombre_usuario= message.from_user.first_name
    cid= message.chat.id               
    if usuario.id in autorizados:
        start_message= '''Bienvenido al bot de Gestión del Grupo 10\nUtilice el comando /help para ver las opciones disponibles.'''
        bot.send_message(cid, start_message)
        log= open('../log/log.txt','a')
        log.write(nombre_usuario+' se ha conectado al bot: '+time.strftime('%c')+'\n')
        log.close()
    else:
        denegacion= "No tiene autorización para hacer uso de este Bot"
        log= open('../log/log.txt','a','utf-8')
        mensaje_denegacion_log= nombre_usuario+' se ha intentado conectar al bot: '+time.strftime('%c')+'\n\n'
        log.write(mensaje_denegacion_log)
        log.close()
        bot.send_message(cid, denegacion)
        bot.send_message(chat_id, mensaje_denegacion_log)
               
@bot.message_handler(commands=['help'])
def help_handler(message):
    usuario= message.from_user
    cid= message.chat.id             
    if usuario.id in autorizados:
        help_message= '''Aquí tiene los comandos implementados para la gestión del switch HP-ProCurve:\n/system get - Devuelve la localización, el nombre, el tiempo en marcha y la persona de contacto del sistema.\n/system set - Configura la localización, el nombre y la persona de contacto del sistema.\n/system set localizacion <localizacion>\n/system set nombre <nombre>\n/system set contacto <contacto>\n/fdb - Devuelve la forwarding database\n/frames - Devuelve una gráfica con las tramas del nivel de enlace por puerto.\n/packages - Devuelve el número de paquetes totales por puerto.\n/port list - Devuelve un listado con el estado de los puertos\n/port get <nºpuerto> - Devuelve el estado del puerto pedido.\n/port set <nºpuerto> <estado(up o down)> - Configura el estado de un puerto.\n/log Obtener el log\n'''
        bot.send_message(cid, help_message)
    else:
        denegacion= "No tiene autorización para hacer uso de este Bot"
        bot.send_message(cid, denegacion)
             
@bot.message_handler(commands=['system'])
def system_handler(message):
    usuario= message.from_user
    cid= message.chat.id
    if usuario.id in autorizados:
        parametros= message.text.split()
        try: 
            if parametros[1]== 'get':
                location= next(getCmd(motor_snmp, comunidad,target_agente,ContextData(),
                             ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0))))
                location_string=str(location[3][0]).split('=')
                coordenadas= location_string[1].split(',')
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
                    print(parametros[3])
                    location_string=str(location[3][0]).split('=')
                    coordenadas= location_string[1].split(',')
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
    else:
        denegacion= "No tiene autorización para hacer uso de este Bot"
        bot.send_message(cid, denegacion)     
        
@bot.message_handler(commands=['fdb'], content_types=['text'])
def fdb_handler(message):
    usuario= message.from_user
    cid= message.chat.id
    if usuario.id in autorizados:
        contador= 0
        peticion_contador= nextCmd(motor_snmp, comunidad, target_agente, ContextData(),ObjectType(ObjectIdentity('BRIDGE-MIB','dot1dTpFdbAddress')))
        variable_bucle= True
        while(variable_bucle):
            peticion_next= next(peticion_contador)
            peticion_next_string= (str(peticion_next[3][0]).split('='))[0].split('.')[0]
            if 'BRIDGE-MIB::dot1dTpFdbAddress' == peticion_next_string:
                contador=contador+1
            else:
                variable_bucle= False
        tablaStr=''
        peticion= bulkCmd(motor_snmp, comunidad, target_agente, ContextData(), 0, contador,
                                ObjectType(ObjectIdentity('BRIDGE-MIB','dot1dTpFdbAddress')), 
                                 ObjectType(ObjectIdentity('BRIDGE-MIB','dot1dTpFdbPort')),
                                 ObjectType(ObjectIdentity('BRIDGE-MIB','dot1dTpFdbStatus')))
        for i in range(contador):
            fdbTable= next(peticion)
            answer= fdbTable[3]
            fila= '['+'\''+str(answer[0]).split('=')[1]+'\''+','+'\''+ str(str(answer[1]).split('=')[1])+'\''+','+'\''+ str(str(answer[2]).split('=')[1])+'\''+']'
            tablaStr= tablaStr+fila+','
        
        fdb= open('../tmp/fdb.html','w')
        pagina_fdb= '''<!DOCTYPE html><html>
      <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Fdb</title>
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css">
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js"></script>
      <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js"></script> 
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
          google.charts.load('current', {'packages':['table']});
          google.charts.setOnLoadCallback(drawTable);
    
          function drawTable() {
            var data = new google.visualization.DataTable();
            data.addColumn('string', 'dot1dTpFdbAddress');
            data.addColumn('string', 'dot1dTpFdbPort');
            data.addColumn('string', 'dot1dTpFdbStatus');
            data.addRows(['''+tablaStr+'''
            ]);
    
            var table = new google.visualization.Table(document.getElementById('table_div'));
    
            table.draw(data, {showRowNumber: false, width: '100%', height: '100%'});
          }
        </script>
      </head>
      <body>
          <div class="container-fluid">
        <h1>Tabla de direcciones MAC aprendidas por el switch</h1>
        <div id="table_div" ></div></div>
      </body>
    </html>'''
        fdb.write(pagina_fdb)
        fdb.close()
        fdb= open('../tmp/fdb.html','r')
        
        bot.send_document(cid,fdb)
    else:
        denegacion= "No tiene autorización para hacer uso de este Bot"
        bot.send_message(cid, denegacion) 

@bot.message_handler(commands=['frames'], content_types=['text'])
def frame_handler(message):
    usuario= message.from_user
    cid= message.chat.id
    if usuario.id in autorizados:
        in_frames='1.3.6.1.2.1.17.4.4.1.3.'
        out_frames='1.3.6.1.2.1.17.4.4.1.4.'
        n_puertos=26
        datos=''
        i=1
        coma=','
        
        while i <= n_puertos:
            indice=str(i)
            campo_in=in_frames+indice
            peticion_in= next(getCmd(motor_snmp, comunidad,target_agente,ContextData(),
                             ObjectType(ObjectIdentity(campo_in))))
            
            frames_in_counter= str(peticion_in[3][0]).split('=')[1]
            frames_in_integer=int(pysnmp.proto.rfc1902.Counter32(frames_in_counter))
            
            campo_out=out_frames+indice
            peticion_out= next(getCmd(motor_snmp, comunidad,target_agente,ContextData(),
                             ObjectType(ObjectIdentity(campo_out))))
            
            frames_out_counter= str(peticion_out[3][0]).split('=')[1]
            frames_out_integer=int(pysnmp.proto.rfc1902.Counter32(frames_out_counter))
               
            datos=datos+str([indice,frames_in_integer,frames_out_integer])
            datos=datos+coma
             
            i=i+1
        print(datos)
        f= open('../tmp/frames.html','w')
        pagina='''<!DOCTYPE html><html>
          <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Frames</title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js"></script> 
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
              google.charts.load('current', {'packages':['bar']});
              google.charts.setOnLoadCallback(drawChart);
    
              function drawChart() {
                var data = google.visualization.arrayToDataTable([
                  ['Puerto', 'Tramas Entrantes', 'Tramas Salientes'],
                  '''+datos+'''
                ]);
    
                var options = {
                  chart: {
                    title: 'Tramas de nivel de enlace por puerto',
                    subtitle: 'HP ProCurve',
                  }
                };
    
                var chart = new google.charts.Bar(document.getElementById('columnchart_material'));
    
               chart.draw(data, google.charts.Bar.convertOptions(options));
              }
            </script>
          </head>
          <body><div class="container-fluid">
            <div id="columnchart_material" style="width: 800px; height: 500px;"></div></div>
          </body>
        </html>
        '''   
        
        f.write(pagina)
        f.close()
    
        f= open('../tmp/frames.html','r')
        
        bot.send_document(cid,f)
    else:
        denegacion= "No tiene autorización para hacer uso de este Bot"
        bot.send_message(cid, denegacion) 
    
@bot.message_handler(commands=['packages'], content_types=['text'])
def packages_handler(message):   
    usuario= message.from_user
    cid= message.chat.id
    if usuario.id in autorizados:
        estado='1.3.6.1.2.1.16.1.1.1.21.'
        datasource='1.3.6.1.2.1.2.2.1.1.'
        paquetes='1.3.6.1.2.1.16.1.1.1.5.'
        n_puertos=26
        datos=''
        i=1
        coma=','
        
        while i<=n_puertos:
            
            puerto=str(i)
            
            #Actualizamos al siguiente puerto
            
            datasourcei=datasource+puerto
            estadoi=estado+puerto
            paquetesi=paquetes+puerto
            
            datasource_oid= pysnmp.proto.rfc1902.ObjectIdentifier(datasourcei)
            #Indicamos el datsource
            next(setCmd(motor_snmp, comunidad,target_agente,ContextData(),
                             ObjectType(ObjectIdentity('RMON-MIB','etherStatsDataSource'),datasource_oid)))
            
            #Indicamos que queremos hacer la peticion
            next(setCmd(motor_snmp, comunidad,target_agente,ContextData(),
                             ObjectType(ObjectIdentity(estadoi),pysnmp.proto.rfc1902.Integer(2)))) 
            
            
            paquetesi=next(getCmd(motor_snmp, comunidad,target_agente,ContextData(),
                             ObjectType(ObjectIdentity(paquetesi))))
        
            
        
            paquetes_string= str(paquetesi[3][0]).split('=')[1]
            paquetes_integer=int(paquetes_string)
               
            datos=datos+str([puerto,paquetes_integer])
            datos=datos+coma
        
            i=i+1
            
        f= open('../tmp/paquetes.html','w')
        pagina='''<!DOCTYPE html><html>
          <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Paquetes</title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js"></script> 
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
              google.charts.load('current', {'packages':['bar']});
              google.charts.setOnLoadCallback(drawChart);
    
              function drawChart() {
                var data = google.visualization.arrayToDataTable([
                  ['Puerto', 'Paquetes Entrantes'],
                  '''+datos+'''
                ]);
    
                var options = {
                  chart: {
                    title: 'Paquetes recibidos por puerto',
                    subtitle: 'HP ProCurve',
                  }
                };
    
                var chart = new google.charts.Bar(document.getElementById('columnchart_material'));
    
               chart.draw(data, google.charts.Bar.convertOptions(options));
              }
            </script>
          </head>
          <body><div class="container-fluid">
            <div id="columnchart_material" style="width: 800px; height: 500px;"></div></div>
          </body>
        </html>
        '''       
        
        f.write(pagina)
        f.close()
    
        f= open('../tmp/paquetes.html','r')
        
        bot.send_document(cid,f)
    else:
        denegacion= "No tiene autorización para hacer uso de este Bot"
        bot.send_message(cid, denegacion)
                 
@bot.message_handler(commands=['port'], content_types=['text'])
def port_handler (message):
    usuario= message.from_user
    cid= message.chat.id
    if usuario.id in autorizados:
        parametros= message.text.split()
        no_puertos= 26
        
        try:
            try: 
                if parametros[1]== 'list':
                    peticion_port= nextCmd(motor_snmp, comunidad,target_agente,ContextData(),
                                 ObjectType(ObjectIdentity('IF-MIB','ifIndex')),ObjectType(ObjectIdentity('IF-MIB','ifOperStatus')))
                    for i in range(no_puertos):
                        peticion_port_next= next(peticion_port)
                        respuesta_indice= str(peticion_port_next[3][0]).split('=')[1]
                        respuesta_status= str(peticion_port_next[3][1]).split('=')[1]
                        
                        up= 'up'
                        down='down'
                        uno= '1'
                        dos='2'
                        
                        if respuesta_status==uno:
                            respuesta_status= up
                        elif respuesta_status==dos:
                            respuesta_status=down
                        
                        port_list_answer= 'Puerto '+respuesta_indice+':'+respuesta_status
                        bot.send_message(cid, port_list_answer)
                            
                elif parametros[1]=='get':
                    get_oid= '1.3.6.1.2.1.2.2.1.8.' 
                    peticion_port= getCmd(motor_snmp, comunidad, target_agente, ContextData(),ObjectType(ObjectIdentity(get_oid+parametros[2])))
                    peticion_port_next= next(peticion_port)
                    respuesta_status= str(peticion_port_next[3][0]).split('=')[1]
                    
                    up= 'up'
                    down='down'
                    uno= '1'
                    dos='2'
                    
                    if respuesta_status==uno:
                        respuesta_status= up
                    elif respuesta_status==dos:
                        respuesta_status=down
                          
                    port_get_answer= 'Puerto '+parametros[2]+':'+respuesta_status
                    bot.send_message(cid, port_get_answer)
                elif parametros[1]=='set':
                    
                    if parametros[3]=='up':
                        conversion=1
                    elif parametros[3]=='down':
                        conversion=2
                    oid_admin= '1.3.6.1.2.1.2.2.1.7.'
                    escalar=pysnmp.proto.rfc1902.Integer(conversion)
                    peticion_port= setCmd(motor_snmp, comunidad, target_agente, ContextData(),ObjectType(ObjectIdentity(oid_admin+parametros[2]),escalar))
                    peticion_port_next= next(peticion_port)
                    respuesta_status= str(peticion_port_next[3][0]).split('=')[1]
                    port_set_answer= 'Puerto '+parametros[2]+':'+respuesta_status
                    bot.send_message(cid, port_set_answer)
                else:
                    bot.send_message(cid, 'Comando no reconocido. Consulte /help') 
            except(StopIteration):
                bot.send_message(cid,'No se ha podido completar el listado')
        except(IndexError):
            bot.send_message(cid, 'Comando incompleto. Consulte /help')
    else:
        denegacion= "No tiene autorización para hacer uso de este Bot"
        bot.send_message(cid, denegacion) 
    
@bot.message_handler(commands=['log'], content_types=['text'])
def log_handler(message):
    cid= message.chat.id
    file= open('../log/log.txt','r')
    bot.send_document(cid, file)
           
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    usuario= message.from_user
    if usuario.id in autorizados:
        mensaje= "Hola "+message.from_user.first_name+"!! ¿En qué puedo ayudarte?. Consulta /help para saber qué soy capaz de hacer"
        bot.reply_to(message, mensaje)
    else:
        denegacion= "No tiene autorización para hacer uso de este Bot"
        bot.reply_to(message, denegacion)
                 

def trap_handler():
    class MyUDPHandler(socketserver.BaseRequestHandler):
        def handle(self):
            data = self.request[0].strip()             
            msgVer = int(api.decodeMessageVersion(data))
            if msgVer in api.protoModules:
                pMod = api.protoModules[msgVer]
                 
            reqMsg, data = decoder.decode(data, asn1Spec=pMod.Message(),)
            reqPDU = pMod.apiMessage.getPDU(reqMsg)
            if reqPDU.isSameTypeWith(pMod.TrapPDU()):
                if msgVer == api.protoVersion1:
                    agente= 'Agent   Address: '+(pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint())
                    trap_generico= 'Generic Trap: '+ (pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint())
                    trap_especifico= 'Specific Trap: '+ (pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint())
                    timestamp= 'Uptime: '+ (pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint())
                    trap=agente+'\n'+trap_generico+'\n'+trap_especifico+'\n'+timestamp
                    mandar_traps(trap)
            return
    if __name__ == "__main__":
        HOST, PORT = '0.0.0.0', 162
        with socketserver.UDPServer((HOST, PORT), MyUDPHandler)as server:
            server.allow_reuse_address= True
            server.serve_forever()
        
def mandar_traps(text):
    chat_id= -172569293
    bot.send_message(chat_id, str(text))
    
def main():
    hilo= threading.Thread(target=trap_handler)
    hilo.start()
    bot.polling()
main()  