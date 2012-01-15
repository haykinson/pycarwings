from xml.dom import minidom
import time
import sha
from datetime import datetime
from datetime import timedelta

from connection import Connection, AuthException
from xmlhelper import dict_to_xml
from response import *

class VehicleService(object):
    """
    Contains commands that are issued to the car 
    to initiate certain actions. Use UserService to retrieve
    action status, however.
    """

    SERVICE_PATH = '/vehicleService'

    namespaces = {'ns4':'urn:com:airbiquity:smartphone.vehicleservice:v1',
                  'ns3':'urn:com:hitachi:gdc:type:vehicle:v1',
                  'ns2':'urn:com:hitachi:gdc:type:portalcommon:v1'}

    def __init__(self, connection):
        self.connection = connection

    def _isoformat(self, date):
        return date.strftime('%Y-%m-%dT%H:%M:%SZ')

    def _vinheader(self, vin):
        return {'ns2:VIN': vin}

    def _post(self, data, root_node):
        xml = dict_to_xml(data, root_node, VehicleService.namespaces)

        self.connection.post_xml(self.SERVICE_PATH, xml, True)
        return True

    def _require_login(self):
        if not self.connection.logged_in:
            raise AuthException('Please log in first')


    def request_status(self, vin):
        self._require_login()

        d = {'ns3:BatteryStatusCheckRequest': 
              {'ns3:VehicleServiceRequestHeader': self._vinheader(vin)}}
                 
        return self._post(d, 'ns4:SmartphoneRemoteBatteryStatusCheckRequest')
    
    def start_charge(self, vin):
        self._require_login()

        d = {'ns3:BatteryRemoteChargingRequest':
                 {'@type':'vehicle:BatteryRemoteChargingRequestType',
                  'ns3:VehicleServiceRequestHeader': self._vinheader(vin),
                  'ns3:NewBatteryChargeRequest':
                      {'ns3:ExecuteTime': self._isoformat(datetime.utcnow())}}}

        return self._post(d, 'ns4:SmartphoneRemoteBatteryChargeRequest')

    def start_ac_now(self, vin):
        return self.start_ac_date(vin, datetime.utcnow() - timedelta(days=60))

    def start_ac_date(self, vin, when):
        self._require_login()

        d = {'ns3:ACRemoteRequest':
                 {'ns3:VehicleServiceRequestHeader': self._vinheader(vin),
                  'ns3:NewACRemoteRequest':
                      {'ns3:ExecuteTime': self._isoformat(when)}}}

        return self._post(d, 'ns4:SmartphoneRemoteACTimerRequest')

    def cancel_ac_now(self, vin):
        self._require_login()

        d = {'ns3:ACRemoteOffRequest': 
              {'ns3:VehicleServiceRequestHeader': self._vinheader(vin)}}

        return self._post(d, 'ns4:SmartphoneRemoteACOffRequest')


    def cancel_ac_date(self, vin):
        self._require_login()

        d = {'ns3:ACRemoteRequest':
                 {'ns3:VehicleServiceRequestHeader': self._vinheader(vin),
                  'ns3:CancelACRemoteRequest': {}}}

        return self._post(d, 'ns4:SmartphoneRemoteACTimerRequest')
