from xml.dom import minidom
import time
import sha

from connection import Connection, AuthException
from xmlhelper import dict_to_xml
from response import *

class UserService(object):

    SERVICE_PATH = '/userService'
    
    def __init__(self, connection):
        self.connection = connection

    def login_and_get_status(self):
        namespaces = {'ns2':'urn:com:airbiquity:smartphone.userservices:v1'}
        d = {'SmartphoneLoginInfo':
                 { 'UserLoginInfo':
                       { 'userId': self.connection.username,
                         'userPassword': self.connection.password },
                   'DeviceToken': 'DUMMY%f' % time.time(),
                   'UUID': sha.sha("carwings_api:%s" % self.connection.username).hexdigest(),
                   'Locale': 'US',
                   'AppVersion': '1.40',
                   'SmartphoneType': 'IPHONE'},
             'SmartphoneOperationType': 'SmartphoneLatestBatteryStatusRequest'}

        xml = dict_to_xml(d, 
                          'ns2:SmartphoneLoginWithAdditionalOperationRequest', 
                          namespaces)

        result = self.connection.post_xml(self.SERVICE_PATH, xml)
        status = LoginStatus(result)
        if status.logged_in:
            self.connection.logged_in = True
        else:
            self.connection.logged_in = False

        return status

    def get_latest_status(self, vin):
        if not self.connection.logged_in:
            raise AuthException('Please log in before checking status')

        namespaces = {'ns2':'urn:com:airbiquity:smartphone.userservices:v1'}
        d = {'VehicleInfo':
                 {'Vin': vin},
             'SmartphoneOperationType': 'SmartphoneLatestBatteryStatusRequest',
             'changeVehicle': 'false'}

        xml = dict_to_xml(d, 
                          'ns2:SmartphoneGetVehicleInfoRequest',
                          namespaces)

        result = self.connection.post_xml(self.SERVICE_PATH, xml)
        return LatestBatteryStatus(result)

    
        
