import pysnmp
from pysnmp.hlapi import *

g = sendNotification(SnmpEngine(), CommunityData('public'),UdpTransportTarget(('192.168.1.225', 162)),ContextData(),'trap',NotificationType(ObjectIdentity('IF-MIB', 'linkDown')))
a=next(g)
print(a)