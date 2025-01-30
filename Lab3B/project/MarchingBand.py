from Lab3B.project.collect_us_sensor_data import US_SENSOR
from utils import sound
from utils.brick import *
import time
import threading
import FluteSensors

motor = Motor("A")
US_SENSOR_STOP = EV3UltrasonicSensor(...)
US_SENSOR_DRUM = EV3UltrasonicSensor(...)

wait_ready_sensors()

stopEvent = threading.Event()

threshold = 10 # How close to trigger the STOP mechanism

def emergencyStop(t):
    while not stopEvent.is_set():
        distance = US_SENSOR.get_cm()
        if distance < threshold:
            stopEvent.set()
        time.sleep(.2)

def drums():
    try:
        while not stopEvent.is_set():
            motor.set_dps(dps=1000)
            motor.set_position_relative(90)
            time.sleep(0.5)
            motor.set_position_relative(-90)
            time.sleep(0.5)
            motor.set_position_relative(90)
            time.sleep(0.3)
            motor.set_position_relative(-90)
            time.sleep(0.3)
            motor.set_position_relative(90)
            time.sleep(0.8)
            motor.set_position_relative(-90)
        motor.set_power(0)
    except BaseException:
        motor.set_power(0)
        exit()


if __name__ == '__main__':
    fluteThread = threading.Thread(target=FluteSensors.fluteSensors)
    # fluteThread.daemon = True
    fluteThread.start()
    emergencyThread = threading.Thread(target=emergencyStop, daemon=True)
    emergencyThread.start()
    FluteSensors.initializeFlute()
    drumOn = False
    while not stopEvent.is_set():
        d = US_SENSOR_DRUM.get_cm()
        if d < threshold:
            drumOn = True
            drumThread = threading.Thread(target=drums, daemon=True)
            drumThread.start()

    if drumThread:
        drumThread.join()

    fluteThread.join()






