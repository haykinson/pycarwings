import sys
from connection import Connection
from userservice import UserService
from vehicleservice import VehicleService

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: %s username password" % sys.argv[0]
        exit(2)

    c = Connection(sys.argv[1], sys.argv[2])
    u = UserService(c)
    print "logging in..."
    d = u.login_and_get_status()
    vin = d.user_info.vin
    print "logged in, vin: %s, nickname: %s" % (vin, d.user_info.nickname)
    v = VehicleService(c)
    print "requesting status..."
    v.request_status(vin)
    print "getting latest..."
    d = u.get_latest_status(vin)
    print "done!"
    import yaml
    print yaml.dump(d)
