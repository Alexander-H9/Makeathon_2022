"""Controll the stepper motor"""
import time
from RPi import GPIO

# use BCM GPIO pin references
GPIO.setmode(GPIO.BCM)
# disable warnings
GPIO.setwarnings(False)

class Stepper():
    """
    Class representing a Stepper Motor
    """
    def __init__(self, sequence="SEQ8", timeout=0.002):
        self.SEQ4 = [[1,0,0,0],
                    [0,1,0,0], 
                    [0,0,1,0], 
                    [0,0,0,1]]

        self.SEQ8 = [[1,0,0,0],
                    [1,1,0,0],
                    [0,1,0,0],
                    [0,1,1,0],
                    [0,0,1,0],
                    [0,0,1,1],
                    [0,0,0,1],
                    [1,0,0,1]]

        if sequence=="SEQ8":
            self.sequence = self.SEQ8
        elif sequence=="SEQ4":
            self.sequence=self.SEQ4
        self.timeout = timeout

        # set all pins as outputs
        self.pins = [24,25,8,7]
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

    def run(self, deg, direc):
        """
        Run the stepper Motor
        """
        cntr = 0
        steps = len(self.sequence)
        n_steps = int(deg*(4096/360)) if steps == 8 else int(deg*(2048/360))

        for i in range(n_steps):
            for j in range(4):
                pin = self.pins[j]
                if self.sequence[cntr][j] != 0:
                    GPIO.output(pin, True)
                else:
                    GPIO.output(pin, False)
            cntr += direc
            if cntr == steps:
                cntr = 0
            if cntr < 0:
                cntr = steps-1
            time.sleep(self.timeout)

if __name__ == '__main__':
    Motor = Stepper()
    Motor.run(180, -1)
