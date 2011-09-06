from xml.dom import minidom
import time
import sha

from connection import Connection, AuthException
from xmlhelper import dict_to_xml
from response import *

class VehicleService(object):

    SERVICE_PATH = '/vehicleService'
    
    def __init__(self, connection):
        self.connection = connection

    def request_status(self, vin):
        if not self.connection.logged_in:
            raise AuthException('Please log in before requesting a status update')

        namespaces = {'ns2':'urn:com:hitachi:gdc:type:portalcommon:v1',
                      'ns3':'urn:com:hitachi:gdc:type:vehicle:v1',
                      'ns4':'urn:com:airbiquity:smartphone.vehicleservice:v1'}
        d = {'ns3:BatteryStatusCheckRequest':
                 {'ns3:VehicleServiceRequestHeader':
                      {'ns2:VIN': vin}}}
        xml = dict_to_xml(d, 'ns4:SmartphoneRemoteBatteryStatusCheckRequest', namespaces)
        result = self.connection.post_xml(self.SERVICE_PATH, xml, True)
        return True
    
        
