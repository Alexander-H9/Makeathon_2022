#!/usr/bin/env python
# coding: utf-8

# import libraries
import time
import RPi.GPIO as GPIO

SEQ8 = [[1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1]]
TIMEOUT = 0.002

# use BCM GPIO pin references
GPIO.setmode(GPIO.BCM)
# disable warnings
GPIO.setwarnings(False)

class Stepper():
    def __init__(self, seq, t):
        self.sequence = seq
        self.timeout = t

        # set all pins as outputs
        self.pins = [24,25,8,7]
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

    def run(self, deg, direc):
        cntr = 0
        steps = len(self.sequence)
        nSteps = int(deg*(4096/360))

        for i in range(nSteps):
            for j in range(4):
                pin = self.pins[j]
                if self.sequence[cntr][j] != 0:
                    GPIO.output(pin, True)
                else:
                    GPIO.output(pin, False)
            cntr += direc
            if (cntr == steps):
                cntr = 0
            if (cntr < 0):
                cntr = steps-1
            time.sleep(self.timeout)

if __name__ == '__main__':
    stepper = Stepper(SEQ8, TIMEOUT)
    stepper.run(180, -1)
