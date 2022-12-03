"""Provides Classes to interact with Makeathon Hardware"""
import time
import json
import requests

IP = "169.254.99.1"

class Sensor:
    """Base class for all Sensors"""
    def __init__(self):
        pass

    def get_data(self, port):
        """Reads Data from Device"""
        url = 'http://' + IP
        portstr = f"/iolinkmaster/port[{port}]/iolinkdevice/pdin/getdata"
        myobj = {"code":"request","cid":4711, "adr":portstr}
        response = requests.post(url, json = myobj, timeout=30)
        return json.loads(response.text)["data"]

class UltrasonicDistance(Sensor):
    """Ultrasonic Distance Sensor"""
    def __init__(self):
        super().__init__()
        self.port = 1

    def get_value(self):
        """Get sensor value from base class"""
        data = self.get_data(self.port)
        val = int(data["value"], 16)>>16
        return val*10/100.0

class TemperatureProbe(Sensor):
    """Temperature Probe Sensor"""
    def __init__(self):
        super().__init__()
        self.port = 2

    def get_value(self):
        """Get sensor value from base class"""
        data = self.get_data(self.port)
        val = int(data["value"], 16)
        return val*10/100.0

class AngleMeasurement(Sensor):
    """Angle Measurement Sensor"""
    def __init__(self):
        super().__init__()
        self.port = 3

    def get_value(self):
        """Get sensor value from base class"""
        data = self.get_data(self.port)
        val = int(data["value"], 16)
        return val

class Capacitor(Sensor):
    """Capacitor Sensor"""
    def __init__(self):
        super().__init__()
        self.port = 4

    def get_value(self):
        """Get sensor value from base class"""
        data = self.get_data(self.port)
        val = int(data["value"], 16)
        return val

class LaserDistance(Sensor):
    """Laser Distance Sensor"""
    def __init__(self):
        super().__init__()
        self.port = 5

    def get_value(self):
        """Get sensor value from base class"""
        data = self.get_data(self.port)
        val = int(data["value"], 16) >> 4
        return val

class Inductor(Sensor):
    """Induction Sensor"""
    def __init__(self):
        super().__init__()
        self.port = 7

    def get_value(self):
        """Get sensor value from base class"""
        data = self.get_data(self.port)
        val = int(data["value"], 16)>>16
        return val

class Socket:
    """This Class provides all the needed Methods to interact with the Socket"""
    def __init__(self):
        self.port = 8

    def get_port(self):
        """Get port"""
        url = 'http://' + IP
        portstr = f"/iolinkmaster/port[{self.port}]/iolinkdevice/pdout/getdata"
        myobj = {"code":"request","cid":4711, "adr":portstr}
        x = requests.post(url, json = myobj, timeout=30)
        y = json.loads(x.text)
        val = int(y["data"]["value"])
        return val

    def set_port(self, val):
        """Set port"""
        url = 'http://' + IP
        portstr = f"/iolinkmaster/port[{self.port}]/iolinkdevice/pdout/setdata"
        valstr = f"{val:02d}"
        myobj = {"code":"request","cid":4712, "adr":portstr, "data":{"newvalue":valstr}}
        requests.post(url, json = myobj, timeout=30)
        return val


if __name__ == "__main__":
    noiseDistance = UltrasonicDistance()
    print("Ultrasonic Distance: ")
    print(noiseDistance.get_value())

    temperature = TemperatureProbe()
    print("Temperature: ")
    print(temperature.get_value())

    angle = AngleMeasurement()
    print("Angle: ")
    print(angle.get_value())

    capacity = Capacitor()
    print("Capacity: ")
    print(capacity.get_value())

    laserDistance = LaserDistance()
    print("Laser Distance: ")
    print(laserDistance.get_value())

    inductor = Inductor()
    print("Induction: ")
    print(inductor.get_value())

    socket = Socket()
    for i in range(2)[::-1]:
        socket.set_port(i)
        print("Socket: ")
        print(socket.get_port())
        time.sleep(1)
    