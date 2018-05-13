import socketserver

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
import subprocess
import asyncio.subprocess
from asyncio.events import AbstractEventLoop




class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        print(data)             
        msgVer = int(api.decodeMessageVersion(data))
        if msgVer in api.protoModules:
            pMod = api.protoModules[msgVer]
             
        reqMsg, data = decoder.decode(data, asn1Spec=pMod.Message(),)
        reqPDU = pMod.apiMessage.getPDU(reqMsg)
        if reqPDU.isSameTypeWith(pMod.TrapPDU()):
            if msgVer == api.protoVersion2c:
                agente= 'Agent   Address: '+(pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint())
                trap_generico= 'Generic Trap: '+ (pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint())
                trap_especifico= 'Specific Trap: '+ (pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint())
                timestamp= 'Uptime: '+ (pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint())
                trap=agente+'\n'+trap_generico+'\n'+trap_especifico+'\n'+timestamp
                chat_id= -172569293
                print(trap)
                    #bot.send_message(chat_id, trap)
                    #varBinds = pMod.apiTrapPDU.getVarBinds(reqPDU)
                #else:
                    #varBinds = pMod.apiPDU.getVarBinds(reqPDU)
#                 print('Var-binds:')
#                 for oid, val in varBinds:
#                     print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))
        return
if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 162
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler)as server:
        server.allow_reuse_address= True
        server.serve_forever()