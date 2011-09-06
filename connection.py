import urllib2
from xml.dom import minidom

class Connection(object):
    """Maintains a connection to CARWINGS, refreshing it when needed"""

    BASE_URL = 'https://nissan-na-smartphone-biz.viaaq.com/aqPortal/smartphoneProxy'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.logged_in = False
        self.connect()

    def connect(self):
        self.handler = urllib2.HTTPCookieProcessor()
        self.opener = urllib2.build_opener(self.handler)

    def post_xml(self, service, xml_data, suppress_response=False):
        data = xml_data.toxml()
        request = urllib2.Request("%s%s" % (self.BASE_URL, service), 
                                  data, 
                                  {'Content-Type': 'text/xml', 
                                   'User-Agent': 'NissanLEAF/1.40 CFNetwork/485.13.9 Darwin/11.0.0 pyCW'})
        response = self.opener.open(request)
        response_data = response.read()
        response.close()
        if not suppress_response:
            return minidom.parseString(response_data)
        else:
            return True


class AuthException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
