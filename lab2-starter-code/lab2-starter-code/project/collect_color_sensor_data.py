#!/usr/bin/env python3

"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

# Add your imports here, if any
from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor


COLOR_SENSOR_DATA_FILE = "../data_analysis/color_sensor.csv"

# complete this based on your hardware setup
color = EV3ColorSensor(...)
t = TouchSensor(...)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.


def collect_color_sensor_data():
    "Collect color sensor data."
    output_file = open(COLOR_SENSOR_DATA_FILE, "w")
    try:
        while not t.is_pressed():
            pass
        if (t.is_pressed()):
            rgb_data = color.get_rgb()
            output_file.write(rgb_data)
            output_file.write("\n")
    except BaseException:
        exit()
    output_file.close()



if __name__ == "__main__":
    collect_color_sensor_data()
