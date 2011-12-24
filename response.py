import iso8601
from xml.dom import minidom
from datetime import timedelta

class XMLResponse(object):
    def get_first(self, node, tag):
        found = node.getElementsByTagNameNS('*', tag)
        if len(found) > 0:
            return found[0]
        else:
            return None

    def get_value(self, node, tag):
        n = self.get_first(node, tag)
        if n and n.firstChild:
            return n.firstChild.data
        else:
            return None

    def get_date_value(self, node, tag):
        d = self.get_value(node, tag)
        return iso8601.parse_date(d) if d else None

class LoginStatus(XMLResponse):
    def __init__(self, data):
        self.parse(data)

    def parse(self, data):
        error = self.get_first(data, 'ErrorCode')
        if not error:
            self.logged_in = True
            user_info = self.get_first(data, 'SmartphoneUserInfoType')
            # latest_battery_status = self.get_first(data, 'SmartphoneLatestBatteryStatusResponse')

            self.user_info = SmartphoneUserInfoType(user_info)
            # self.latest_battery_status = SmartphoneLatestBatteryStatusResponse(latest_battery_status)
        else:
            self.logged_in = False

class LatestBatteryStatus(XMLResponse):
    def __init__(self, data):
        self.parse(data)

    def parse(self, data):
        latest_battery_status = self.get_first(data, 'SmartphoneLatestBatteryStatusResponse')

        self.latest_battery_status = SmartphoneLatestBatteryStatusResponse(latest_battery_status)

class SmartphoneUserInfoType(XMLResponse):
    def __init__(self, data):
        self.parse(data)

    def parse(self, data):
        self.nickname = self.get_value(data, 'Nickname')
        self.vin = self.get_value(data, 'Vin')
        return self

class SmartphoneLatestBatteryStatusResponse(XMLResponse):
    def __init__(self, data):
        self.parse(data)

    def parse(self, data):
        status = self.get_first(data, 'BatteryStatusRecords')
        
        self.operation_result = self.get_value(status, 'OperationResult')
        self.operation_date_and_time = self.get_date_value(status, 'OperationDateAndTime')
        self.battery_charging_status = self.get_value(status, 'BatteryChargingStatus')
        self.battery_capacity = self.get_value(status, 'BatteryCapacity')
        self.battery_remaining_amount = self.get_value(status, 'BatteryRemainingAmount')
        self.plugin_state = self.get_value(status, 'PluginState')
        self.cruising_range_ac_on = self.get_value(status, 'CruisingRangeAcOn')
        self.cruising_range_ac_off = self.get_value(status, 'CruisingRangeAcOff')

        time_required_to_full = self.get_first(status, 'TimeRequiredToFull')
        if time_required_to_full:
            #parse time required to full
            hour_required_to_full = int(self.get_value(time_required_to_full, 'HourRequiredToFull'))
            minutes_required_to_full = int(self.get_value(time_required_to_full, 'MinutesRequiredToFull'))
        
            self.time_required_to_full = timedelta(hours=hour_required_to_full,
                                                   minutes=minutes_required_to_full)
        else:
            self.time_required_to_full = None

        time_required_to_full_L2 = self.get_first(status, 'TimeRequiredToFull200')
        if time_required_to_full_L2:
            #parse time required to full
            hour_required_to_full_L2 = int(self.get_value(time_required_to_full_L2, 'HourRequiredToFull'))
            minutes_required_to_full_L2 = int(self.get_value(time_required_to_full_L2, 'MinutesRequiredToFull'))
        
            self.time_required_to_full_L2 = timedelta(hours=hour_required_to_full_L2,
                                                   minutes=minutes_required_to_full_L2)
        else:
            self.time_required_to_full_L2 = None

        self.notification_date_and_time = self.get_date_value(status, 'NotificationDateAndTime')
        
        self.last_battery_status_check_execution_time = self.get_date_value(data, 'lastBatteryStatusCheckExecutionTime')

