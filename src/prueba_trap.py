import pysnmp
from pysnmp.hlapi import *

g = sendNotification(SnmpEngine(), CommunityData('public'),UdpTransportTarget(('10.10.10.2', 162)),ContextData(),'trap',NotificationType(ObjectIdentity('IF-MIB', 'linkDown')))
a=next(g)
print(a)