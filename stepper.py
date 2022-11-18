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
    """
    Class representing a Stepper Motor
    """
    def __init__(self, seq, t):
        self.sequence = seq
        self.timeout = t

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
        n_steps = int(deg*(4096/360))

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
    Motor = Stepper(SEQ8, TIMEOUT)
    # stepper.run(180, -1)

    import threading
    from io_link import Capacitor
    from plot_graphs import plot_2D

    thread_motor = threading.Thread(target=Motor.run, args=(180, -1))
    thread_motor.start()

    data = []
    while thread_motor.is_alive():
        val = Capacitor.get_value()
        if val < 1000:
            data.append(val)

    plot_2D(list(range(len(data))), data)
