import threading

if not __debug__:
    from io_link import Inductor
    from stepper import Stepper

def measurement():
    """Starting stepper motor and measurement"""
    if __debug__:
        return [202,155,645,170]

    Sensor = Inductor()
    Motor = Stepper()

    thread_motor = threading.Thread(target=Motor.run, args=(180, -1))
    thread_motor.start()

    data = []
    while thread_motor.is_alive():
        val = Sensor.get_value()
        if val < 1000:
            data.append(val)
    return data