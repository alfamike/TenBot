import pysnmp
from pysnmp.hlapi import *

g = sendNotification(SnmpEngine(), CommunityData('public'),UdpTransportTarget(('192.168.0.1', 45002)),ContextData(),'trap',NotificationType(ObjectIdentity('IF-MIB', 'linkDown')))
a=next(g)
print(a)