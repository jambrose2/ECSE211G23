from Lab3B.project.collect_us_sensor_data import US_SENSOR
from utils import sound
from utils.brick import *
import time
import threading
import FluteSensors

motor = Motor(...)
cSensor = EV3ColorSensor(...)


wait_ready_sensors()

stopEvent = threading.Event()



def colorIdentifier(rgb):
    s = rgb[0] + rgb[1] + rgb[2]
    if s == 0:
        return 0
    newRGB = [rgb[0]/s, rgb[1]/s, rgb[2]/s]
    if newRGB[0] > 0.6:
        if newRGB[1] < 0.4:
            if newRGB[2] < 0.3:
                return 1
    elif newRGB[1] > 0.5:
        if newRGB[0] < 0.25:
            if newRGB[2] < 0.2:
                return 2
    # elif newRGB[2] > 0.375:
     #   if newRGB[0] < 0.225:
        #    if newRGB[1] < 0.4 and newRGB[1] > 0.1:
             #   return 3
    else:
        print("Unable to identify")
        return 0

def colorLoop(t):
    while not stopEvent.is_set():
        color = cSensor.get_rgb()
        id = colorIdentifier(color)

        if id == 1:
            print("Red")
            if drumOn:
                drumOn = False
                stopEvent.set()
                motor.set_power(0)
                drumThread.join()
                stopEvent.clear()

        elif id == 2:
            print("Green")
            if not drumOn:
                drumOn = True
                stopEvent.clear()
                drumThread = threading.Thread(target=drums)
                drumThread.start()
        # elif colorIdentifier(color) == 3:
        #     print("Blue")
        else:
            print("Unable to identify")
            continue

def drums():
    try:
        while not stopEvent.is_set():
            motor.set_dps(dps=1000)
            motor.set_position_relative(45, block=True)
            time.sleep(0.5)
            motor.set_position_relative(-45, block=True)
            time.sleep(0.5)
            motor.set_position_relative(45, block=True)
            time.sleep(0.3)
            motor.set_position_relative(-45, block=True)
            time.sleep(0.3)
            motor.set_position_relative(45, block=True)
            time.sleep(0.8)
            motor.set_position_relative(-45, block=True)
        motor.set_power(0)
    except Exception as e:
        print("Drums error: ", e)
    finally:
        motor.set_power(0)


if __name__ == '__main__':
    fluteThread = threading.Thread(target=FluteSensors.initializeFlute, daemon=True)
    # fluteThread.daemon = True
    fluteThread.start()
    ColorSensorLoop = threading.Thread(target=colorLoop, daemon=True)
    ColorSensorLoop.start()
    drumOn = False
    
