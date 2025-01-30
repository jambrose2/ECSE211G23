from utils.brick import wait_ready_sensors, TouchSensor
from utils import sound

note1 = sound.Sound(duration=0.3, pitch="G2", volume=80)
note2 = sound.Sound(duration=0.3, pitch="A#0", volume=80)
note3 = sound.Sound(duration=0.3, pitch="C#2", volume=80)
note4 = sound.Sound(duration=0.3, pitch="D#4", volume=80)


touch1 = TouchSensor(1)
touch2 = TouchSensor(2)
touch3 = TouchSensor(3)
touch4 = TouchSensor(4)

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


def initializeFlute():
    try:
        while True:
            if touch1.is_pressed:
                play_sound(1)
            if touch2.is_pressed:
                play_sound(2)
            if touch3.is_pressed:
                play_sound(3)
            if touch4.is_pressed:
                play_sound(4)
    except BaseException or KeyboardInterrupt:
        exit()

if __name__ == '__main__':

    initializeFlute()
