from utils.brick import wait_ready_sensors, TouchSensor, EV3UltrasonicSensor
from utils import sound
import time


# Declare notes with distinct pitches
note1 = sound.Sound(duration=0.3, pitch="F#4", volume=80)
note2 = sound.Sound(duration=0.3, pitch="Bb3", volume=80)
note3 = sound.Sound(duration=0.3, pitch="Eb5", volume=80)
note4 = sound.Sound(duration=0.3, pitch="D#4", volume=80)


# Declare sensors
touch1 = TouchSensor(1)
touch2 = TouchSensor(2)
US = EV3UltrasonicSensor(3)


# Threshold to trigger the ultrasonic sensor
cutoff = 5


# Function that takes int i as argument and plays the associated note
def play_sound(i):
    if (i == 1):
        note1.play()
        note1.wait_done()
    elif (i == 2):
        note2.play()
        note2.wait_done()
    elif (i == 3):
        note3.play()
        note3.wait_done()
    elif (i == 4):
        note4.play()
        note4.wait_done()
    return



# Function to wait for user to play the flute, takes stopEvent as argument
def initializeFlute(stopEvent):
    try:
        # Loop infinitely until emergency stop
        while not stopEvent.is_set():
            # Trigger notes according to sensor input
            if touch1.is_pressed() and touch2.is_pressed():
                play_sound(4)
            elif touch1.is_pressed():
                play_sound(1)
            elif touch2.is_pressed():
                play_sound(2)
            # Check multiple times for ultrasonic distance to not play notes on 
            # faulty readings
            if US.get_cm() < cutoff:
                time.sleep(0.01)
                if US.get_cm() < cutoff:
                    time.sleep(0.01)
                    if US.get_cm() < cutoff:
                        time.sleep(0.1)
                        play_sound(3)
            # Brief sleep to not overload system
            time.sleep(0.05)
            
    # Catch and print exceptions
    except Exception as e:
        print("Error: " + str(e))


# Tester
if __name__ == '__main__':
    initializeFlute()
