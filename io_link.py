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

    def get_value(self):
        y = self.getData(self.port)
        val = int(y["data"]["value"], 16)>>16
        return val*10/100.0

class TemperatureProbe(Sensor):
    def __init__(self):
        super().__init__()
        self.port = 2

    def get_value(self):
        y = self.getData(self.port)
        val = int(y["data"]["value"], 16)
        return val*10/100.0

class AngleMeasurement(Sensor):
    def __init__(self):
        super().__init__()
        self.port = 3

    def get_value(self):
        y = self.getData(self.port)
        val = int(y["data"]["value"], 16)
        return val

class Capacitor(Sensor):
    def __init__(self):
        super().__init__()
        self.port = 4

    def get_value(self):
        y = self.getData(self.port)
        val = int(y["data"]["value"], 16)
        return val

class LaserDistance(Sensor):
    def __init__(self):
        super().__init__()
        self.port = 5

    def get_value(self):
        y = self.getData(self.port)
        val = int(y["data"]["value"], 16) >> 4
        return val

class Inductor(Sensor):
    def __init__(self):
        super().__init__()
        self.port = 7

    def get_value(self):
        y = self.getData(self.port)
        val = int(y["data"]["value"], 16)>>16
        return val

class Socket:
    def __init__(self):
        self.port = 8

    def get_port(self):
        url = 'http://' + IP
        portstr = "/iolinkmaster/port[{}]/iolinkdevice/pdout/getdata".format(self.port)
        myobj = {"code":"request","cid":4711, "adr":portstr}
        x = requests.post(url, json = myobj)
        y = json.loads(x.text)
        val = int(y["data"]["value"])
        return val

    def set_port(self, val):
        url = 'http://' + IP
        portstr = "/iolinkmaster/port[{}]/iolinkdevice/pdout/setdata".format(self.port)
        valstr = "{:02d}".format(val)
        myobj = {"code":"request","cid":4712, "adr":portstr, "data":{"newvalue":valstr}}
        requests.post(url, json = myobj)
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
    