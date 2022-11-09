#!/usr/bin/env python
# coding: utf-8

import requests
import json
import time

IP = "169.254.99.1"

class Sensor:
    def __init__(self):
        pass
    
    def getData(self, port):
        url = 'http://' + IP
        portstr = "/iolinkmaster/port[{}]/iolinkdevice/pdin/getdata".format(port)
        myobj = {"code":"request","cid":4711, "adr":portstr}
        x = requests.post(url, json = myobj)
        y = json.loads(x.text)
        return y

class UltrasonicDistance(Sensor):
    def __init__(self):
        super().__init__()
        self.port = 1

    def getValue(self):
        y = self.getData(self.port)
        val = int(y["data"]["value"], 16)>>16
        return val*10/100.0

class TemperatureProbe(Sensor):
    def __init__(self):
        super().__init__()
        self.port = 2

    def getValue(self):
        y = self.getData(self.port)
        val = int(y["data"]["value"], 16)
        return val*10/100.0

class AngleMeasurement(Sensor):
    def __init__(self):
        super().__init__()
        self.port = 3

    def getValue(self):
        y = self.getData(self.port)
        val = int(y["data"]["value"], 16)
        return val

class Capacitor(Sensor):
    def __init__(self):
        super().__init__()
        self.port = 4

    def getValue(self):
        y = self.getData(self.port)
        val = int(y["data"]["value"], 16)
        return val

class LaserDistance(Sensor):
    def __init__(self):
        super().__init__()
        self.port = 5

    def getValue(self):
        y = self.getData(self.port)
        val = int(y["data"]["value"], 16) >> 4
        return val

class Inductor(Sensor):
    def __init__(self):
        super().__init__()
        self.port = 7

    def getValue(self):
        y = self.getData(self.port)
        val = int(y["data"]["value"], 16)>>16
        return val

class Socket:
    def __init__(self):
        self.port = 8

    def getPort(self):
        url = 'http://' + IP
        portstr = "/iolinkmaster/port[{}]/iolinkdevice/pdout/getdata".format(self.port)
        myobj = {"code":"request","cid":4711, "adr":portstr}
        x = requests.post(url, json = myobj)
        y = json.loads(x.text)
        val = int(y["data"]["value"])
        return val

    def setPort(self, val):
        url = 'http://' + IP
        portstr = "/iolinkmaster/port[{}]/iolinkdevice/pdout/setdata".format(self.port)
        valstr = "{:02d}".format(val)
        myobj = {"code":"request","cid":4712, "adr":portstr, "data":{"newvalue":valstr}}
        requests.post(url, json = myobj)
        return val


if __name__ == "__main__":
    noiseDistance = UltrasonicDistance()
    print("Ultrasonic Distance: ")
    print(noiseDistance.getValue())

    temperature = TemperatureProbe()
    print("Temperature: ")
    print(temperature.getValue())

    angle = AngleMeasurement()
    print("Angle: ")
    print(angle.getValue())

    capacity = Capacitor()
    print("Capacity: ")
    print(capacity.getValue())

    laserDistance = LaserDistance()
    print("Laser Distance: ")
    print(laserDistance.getValue())

    inductor = Inductor()
    print("Induction: ")
    print(inductor.getValue())

    socket = Socket()
    for i in range(2)[::-1]:
        socket.setPort(i)
        print("Socket: ")
        print(socket.getPort())
        time.sleep(1)
    