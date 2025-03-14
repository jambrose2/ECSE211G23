import simpleaudio as sa
import threading
import time


sound = sa.WaveObject.from_wave_file("203913__landub__fire-brigade-siren-street-cars.wav")



def fireSiren():
    while True:
        play_obj = sound.play()
        play_obj.wait_done()
