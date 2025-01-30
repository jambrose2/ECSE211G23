from Lab3B.project.collect_us_sensor_data import US_SENSOR
from utils import sound
from utils.brick import *
import time
import threading
import FluteSensors

motor = Motor("A")
US_SENSOR = EV3UltrasonicSensor(...)
wait_ready_sensors()

stopEvent = threading.Event()

threshold = 10 # How close to trigger the STOP mechanism

def emergencyStop(t):
    while not stopEvent.is_set():
        distance = US_SENSOR.get_distance()
        if distance < threshold:
            stopEvent.set()
        time.sleep(.2)

def drums():
    motor.set_dps(dps=1000)
    motor.


if __name__ == '__main__':
    fluteThread = threading.Thread(target=FluteSensors.fluteSensors)
    # fluteThread.daemon = True
    fluteThread.start()
    emergencyThread = threading.Thread(target=emergencyStop, daemon=True)
    emergencyThread.start()


