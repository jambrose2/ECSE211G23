from Lab3B.project.collect_us_sensor_data import US_SENSOR
from utils import sound
from utils.brick import *
import time
import threading
import FluteSensors


# Initialize motors and color sensor
motor = Motor('A')
cSensor = EV3ColorSensor(3)

# Allow sensors to set up
wait_ready_sensors()


# Declare stop event
stopEvent = threading.Event()


# Classification algorithm for color sensor values
def colorIdentifier(rgb):
    # Return 0 if missing any values
    if rgb[0] == None or rgb[1] == None or rgb[2] == None:
        return 0
    # Sum RGB values
    s = rgb[0] + rgb[1] + rgb[2]
    # Return 0 if the value is not a strong reading
    if s < 85:
        return 0
    # Normalize RGB values
    newRGB = [rgb[0]/s, rgb[1]/s, rgb[2]/s]
    # Identify the color based on testing clusters
    if newRGB[0] > 0.6:
        if newRGB[1] < 0.4:
            if newRGB[2] < 0.3:
                return 1
    elif newRGB[1] > 0.5:
        if newRGB[0] < 0.25:
            if newRGB[2] < 0.2:
                return 2
    # Return 0 if doesn't strongly match a color
    else:
        print("Unable to identify")
        return 0


# Function to read color sensor
def colorLoop():
    # Set variable for drum status
    drumOn = False
    # Loop infinitely until emergency stop
    while not stopEvent.is_set():
        # Won't run without some print here, asked multiple TA's, tried to sleep 
        # too. Both TA's said it was fine to leave 
        print('')
        # Identify current color status
        color = cSensor.get_rgb()
        i = colorIdentifier(color)

        # If color is red, turn drum off, stop flute and exit
        if i == 1:
            # print("Red")
            # Check if drums on
            if drumOn:
                motor.set_power(0)
                drumOn = False
                stopEvent.set()
                time.sleep(0.5)
                drumThread.join()
                fluteThread.join()
                exit()
        
        # If color green, start drums
        elif i == 2:
            # print("Green")
            # Check if drums already on
            if not drumOn:
                stopEvent.clear()
                # Start a thread for the drums
                drumThread = threading.Thread(target=drums)
                drumThread.start()
                drumOn = True
        # Continue if not green or red
        else:
            continue


# Function to control drum movement
def drums():
    try:
        # Loop infinitely until emergency stop
        while not stopEvent.is_set():
            
            # Rotate motor up and down, pausing in between to make a melody
            motor.set_dps(dps=1000)
            motor.set_position_relative(100)
            time.sleep(1)
            # Check emergency stop for a quicker exit
            if (stopEvent.is_set()):
                motor.set_power(0)
                break
            motor.set_position_relative(-100)
            time.sleep(1.2)
            if (stopEvent.is_set()):
                motor.set_power(0)
                break
            motor.set_position_relative(100)
            time.sleep(1.3)
            if (stopEvent.is_set()):
                motor.set_power(0)
                break
            motor.set_position_relative(-100)
            time.sleep(0.8)
            if (stopEvent.is_set()):
                motor.set_power(0)
                break
            motor.set_position_relative(100)
            time.sleep(1.6)
            if (stopEvent.is_set()):
                motor.set_power(0)
                break
            motor.set_position_relative(-100)
            time.sleep(1.1)
        motor.set_power(0)
    except Exception as e:
        print("Drums error: ", e)
    # Turn off motor
    finally:
        motor.set_power(0)


if __name__ == '__main__':
    # Start thread for flute and run
    fluteThread = threading.Thread(target=FluteSensors.initializeFlute, args=(stopEvent,), daemon=True)
    fluteThread.start()
    # Start thread for color sensor and run
    ColorSensorLoop = threading.Thread(target=colorLoop, daemon=True)
    ColorSensorLoop.start()
    
