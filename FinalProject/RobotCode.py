from utils.brick import *
import time
import threading
from utils import sound

forwardSpeedR = 34.3
forwardSpeedL = 34.3
turnRadius = 0
straightDistance = 43
distance = 500
rightDistance = 17
angle = 1000000000
veryFirstangle = 0
currAngle = 0
currentSquare = 0
obstacleSquares = [False, False, False, False, False, False]
fireSquares = [False, False, False, False, False, False]
visited = [False, False, False, False, False, False]
firesPutOut = 0
needBothTop = False


RIGHT_WHEEL = Motor('C')
LEFT_WHEEL = Motor('A')
P = Motor('B')
COLOR_SENSOR_MOTOR = Motor('D')

COLOR_SENSOR_MOTOR.set_limits(50, 1250)

GYRO = EV3GyroSensor(3)
COLOR_SENSOR = EV3ColorSensor(1)
US_SENSOR = EV3UltrasonicSensor(2)

emergencyStopButton = TouchSensor(4)

time.sleep(1)


GYRO.reset_measure()
time.sleep(2.5)

note1 = sound.Sound(duration=0.2, pitch="F#4", volume=100)
note2 = sound.Sound(duration=0.2, pitch="Bb3", volume=100)

US_SENSOR_DATA_FILE = "../us_sensor.csv"
COLOR_SENSOR_DATA_FILE = "../color_sensor.csv"


stopEvent = threading.Event()
fireEvent = threading.Event()


def fireSiren():
    while not fireEvent.is_set():
        note1.play()
        time.sleep(0.15)
        note2.play()
        time.sleep(0.15)
        if (stopEvent.is_set()):
            return

def ultrasonicReader():
    while not stopEvent.is_set():
        distance = US_SENSOR.get_cm()
        time.sleep(0.1)
        print("Distance: ", distance)
        return distance
            #while True:
                #distance = US_SENSOR.get_cm()
            #time.sleep
            #time.sleep(0.1)

def emergencyStop():
    while not emergencyStopButton.is_pressed():
        time.sleep(0.1)
    stopEvent.set()
    while True:
        LEFT_WHEEL.set_power(0)
        RIGHT_WHEEL.set_power(0)
        P.set_power(0)
        COLOR_SENSOR_MOTOR.set_power(0)
        #print("Emergency stop activated")
    


def gyroReader():
    global angle
    global currAngle
    angle = GYRO.get_abs_measure()
    veryFirstAngle = angle
    print("First", angle)
    while not stopEvent.is_set():
        currAngle = GYRO.get_abs_measure()
        print(currAngle)
        time.sleep(.3)
    
def straight():
    global distance
    while True:
        if (stopEvent.is_set()):
            return
        LEFT_WHEEL.set_power(forwardSpeedL)
        RIGHT_WHEEL.set_power(forwardSpeedR)
        time.sleep(1.5)
        distance = ultrasonicReader()
        if distance <= straightDistance + turnRadius + 5:
            LEFT_WHEEL.set_power(0)
            RIGHT_WHEEL.set_power(0)
            #if STOP.is_set():
                #break
            turn90Right(angle)
            return
            #straightRight()
        if distance <= straightDistance + 20:
            LEFT_WHEEL.set_power(0)
            RIGHT_WHEEL.set_power(0)
            #if STOP.is_set():
                #break
            distance = ultrasonicReader()
            for _ in range(10):
                if stopEvent.is_set():
                    return
                LEFT_WHEEL.set_power(forwardSpeedL)
                RIGHT_WHEEL.set_power(forwardSpeedR)
                time.sleep(0.1)
                distance = ultrasonicReader()
                if distance <= straightDistance + turnRadius + 5:
                    LEFT_WHEEL.set_power(0)
                    RIGHT_WHEEL.set_power(0)
                    #if STOP.is_set():
                        #break
                    turn90Right(angle)
                    return
                    #straightRight()
                    

def turn90Left(cAng):
    global currAngle
    global angle
    global stopEvent
    if stopEvent.is_set():
        return
    RIGHT_WHEEL.set_power(forwardSpeedR)
    LEFT_WHEEL.set_power(-forwardSpeedL)
    time.sleep(1.3)
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)
    while currAngle > cAng - 90:
        print(currAngle)
        if stopEvent.is_set():
            return
        RIGHT_WHEEL.set_power(forwardSpeedR/2)
        LEFT_WHEEL.set_power(-forwardSpeedL/2)
        time.sleep(0.1)
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)

def turn90Right(cAng):
    global currAngle
    if stopEvent.is_set():
        return
    RIGHT_WHEEL.set_power(-forwardSpeedR)
    LEFT_WHEEL.set_power(forwardSpeedL)
    time.sleep(2)
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)
    print("Before loop", currAngle)
    while currAngle < cAng + 90:
        if stopEvent.is_set():
            return
        print("Curr", currAngle)
        LEFT_WHEEL.set_power(forwardSpeedL/2)
        RIGHT_WHEEL.set_power(-forwardSpeedR/2)
        time.sleep(0.1)
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)

def corridor():
    global angle
    distance = ultrasonicReader()
    while distance > rightDistance + 20:
        if stopEvent.is_set():
            return
        LEFT_WHEEL.set_power(forwardSpeedL)
        RIGHT_WHEEL.set_power(forwardSpeedR)
        time.sleep(.5)
        distance = ultrasonicReader()
    if distance <= rightDistance + turnRadius:
        distance = ultrasonicReader()
        if distance <= rightDistance + turnRadius:
            LEFT_WHEEL.set_power(0)
            RIGHT_WHEEL.set_power(0)
            if stopEvent.is_set():
                return
            turn90Left(angle + 90)
        distance = ultrasonicReader()
    elif distance <= rightDistance + 20: 
        LEFT_WHEEL.set_power(0)
        RIGHT_WHEEL.set_power(0)
        for _ in range(10):
            if stopEvent.is_set():
                return
            distance = ultrasonicReader()
            LEFT_WHEEL.set_power(forwardSpeedL)
            RIGHT_WHEEL.set_power(forwardSpeedR)
            time.sleep(0.1)
            if distance <= rightDistance + turnRadius + 5:
                if distance <= rightDistance + turnRadius + 5:
                    LEFT_WHEEL.set_power(0)
                    RIGHT_WHEEL.set_power(0)
        turn90Left(angle + 90)
        forward(1)
        time.sleep(1.5)
        stopEvent.set()


def backup(dist):
    if stopEvent.is_set():
        return
    RIGHT_WHEEL.set_power(-forwardSpeedR)
    LEFT_WHEEL.set_power(-forwardSpeedL)
    time.sleep(dist)
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)
    
def get_color():
    if stopEvent.is_set():
        return
    color = COLOR_SENSOR.get_rgb()
    i = colorIdentifier(color)
    return i
            
def colorIdentifier(rgb):
    if stopEvent.is_set():
        return
    if rgb[0] == None or rgb[1] == None or rgb[2] == None:
        return 0
    s = rgb[0] + rgb[1] + rgb[2]
    if (s < 150):
        return 3
    newRGB = [rgb[0]/s, rgb[1]/s, rgb[2]/s]
    if newRGB[0] > 0.55:
        if newRGB[1] < 0.42:
            if newRGB[2] < 0.32:
                print(rgb)
                return 1
    elif newRGB[0] < 0.37:
        if newRGB[1] > 0.55:
            if newRGB[2] < 0.1:
                return 2
    else:
        return 0
    
def extinguishProtocol():
    global currentSquare
    global fireSquares
    global firesPutOut
    fireSquares[currentSquare] = True
    print("ext")
    time.sleep(0.25)
    if stopEvent.is_set():
        return
    COLOR_SENSOR_MOTOR.set_position_relative(90)
    time.sleep(1)
    backup(2)
    COLOR_SENSOR_MOTOR.set_position_relative(-90)
    time.sleep(2)
    time.sleep(0.5)
    P.set_power(-50)
    time.sleep(1)
    P.set_power(0)
    time.sleep(0.25)
    forward(1.8)
    firesPutOut += 1
    if firesPutOut == 2:
        stopEvent.set()
        return

    
def backup(length):
    if stopEvent.is_set():
        return
    RIGHT_WHEEL.set_power(-20)
    LEFT_WHEEL.set_power(-20)
    time.sleep(length)
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)
    
def forward(length):
    if stopEvent.is_set():
        return
    RIGHT_WHEEL.set_power(20)
    LEFT_WHEEL.set_power(20)
    time.sleep(length - 0.2)
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)

    
def fireFind(startAng):
    global currAngle
    global currentSquare
    
    color = 0
    color2 = 0
    for i in range(150):
        if stopEvent.is_set():
            return
        RIGHT_WHEEL.set_power(forwardSpeedR * 0.5)
        LEFT_WHEEL.set_power(-forwardSpeedL * 0.5)
        time.sleep(.09)
        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
        color = get_color()
        if (color == 3):
            RIGHT_WHEEL.set_power(-forwardSpeedR * 0.5)
            LEFT_WHEEL.set_power(forwardSpeedL * 0.5)
            time.sleep(0.29)
            break
        if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
            elif (color2 == 2):
                evade()
                return
    LEFT_WHEEL.set_power(forwardSpeedL * 0.5)
    RIGHT_WHEEL.set_power(-forwardSpeedR * 0.5)
    time.sleep(0.12)
    for i in range(150):
        if stopEvent.is_set():
            return
        LEFT_WHEEL.set_power(forwardSpeedL * 0.5)
        RIGHT_WHEEL.set_power(-forwardSpeedR * 0.5)
        time.sleep(0.09)
        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
        color = get_color()
        if (color == 3):
            LEFT_WHEEL.set_power(-forwardSpeedL * 0.5)
            RIGHT_WHEEL.set_power(forwardSpeedR * 0.5)
            time.sleep(0.3)
            break
        if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
            elif (color2 == 2):
                evade()
                return
    for _ in range(30):
        if stopEvent.is_set():
            return
        if (currAngle > startAng + 9):
            RIGHT_WHEEL.set_power(forwardSpeedR * 0.5)
            LEFT_WHEEL.set_power(-forwardSpeedL * 0.5)
            time.sleep(.1)
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
        else:
            break
    if currentSquare == 3 or currentSquare == 2 or currentSquare == 4:
        if stopEvent.is_set():
            return
        if (ultrasonicReader() < 6):
            backup(1)
            straighten(angle)
            return
    
def fullSquare():
    global currAngle
    global currentSquare
    global angle
    visited[currentSquare] = True
    print("First", angle)
    
    #
    #  Square 0
    while ultrasonicReader() > 35:
        if stopEvent.is_set():
            return
        color = get_color()
        if (color == 1):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
        forward(0.4)
    while (ultrasonicReader() < 36):
        if stopEvent.is_set():
            return
        backup(0.4)
    backup(0.5)
    time.sleep(1)
    color = get_color()
    if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
    if stopEvent.is_set():
        return
    forward(0.44)
    for i in range(4):
        if stopEvent.is_set():
            return
        fireFind(currAngle)
        straighten(angle)
        #if i < 2:
         #   angle = currAngle
        angle += 6
        print("new ang", angle)
        forward(0.45)
        color = get_color()
        if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
    straighten(angle)
    while (ultrasonicReader() > 19):
        if stopEvent.is_set():
            return
        forward(.3)
    currentSquare = 3
    visited[currentSquare] = True
    color = get_color()
    angle = currAngle
    #
    # Back middle square
    if stopEvent.is_set():
        return
    if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
            elif (color2 == 2):
                evade()
                
    forward(0.45)
    straighten(angle)
    for k in range(4):
        if stopEvent.is_set():
            return
        fireFind(currAngle)
        straighten(angle)
        if (ultrasonicReader() < 6.5 or ultrasonicReader() == 255):
            while ultrasonicReader() < 16:
                if stopEvent.is_set():
                    return
                backup(0.4)
                k = 5
            break
        forward(0.4)
        angle = currAngle
        print("new ang", angle)
        color = get_color()
        if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
    straighten(angle)
    if stopEvent.is_set():
        return
    while (ultrasonicReader() < 15):
        backup(0.4)
    turn90Left(angle + 10)
    while (ultrasonicReader() < 60):
        if stopEvent.is_set():
            return
        backup(0.3)
    angle = currAngle
    print('new ang', angle)
    currentSquare = 1
    visited[currentSquare] = True
    color = get_color()
    #
    # Front left square
    straighten(angle)
    if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
            elif (color2 == 2):
                evade()
    if stopEvent.is_set():
        return
    forward(0.65)
    for j in range(4):
        if stopEvent.is_set():
            return
        fireFind(currAngle)
        if (ultrasonicReader() < 40):
            backup(0.3)
            j = 5
            break
        forward(0.65)
        angle = currAngle
        print("new ang", angle)
        straighten(angle)
        color = get_color()
        if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
            elif (color2 == 2):
                evade()
                break
    straighten(angle)
    turn90Right(angle - 10)
    time.sleep(0.5)
    turn90Right(angle - 10)
    angle = currAngle
    while ultrasonicReader() > 20:
        if stopEvent.is_set():
            return
        forward(0.3)
    straighten(angle)
    if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
            elif (color2 == 2):
                evade()
    forward(0.65)
    for j in range(4):
        if stopEvent.is_set():
            return
        fireFind(currAngle)
        if (ultrasonicReader() < 6.5 or ultrasonicReader() == 255):
            backup(0.3)
            j = 5
            break
        angle = currAngle
        print("new ang", angle)
        forward(0.65)
        straighten(angle)
        color = get_color()
        if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
            elif (color2 == 2):
                evade()
                break
    while ultrasonicReader() < 20:
        if stopEvent.is_set():
            return
        backup(0.3)
    turn90Right(angle)
    #
    # Back right square 
    

def straighten(a):
    global currAngle
    while currAngle > a + 2:
        if stopEvent.is_set():
            return
        RIGHT_WHEEL.set_power(forwardSpeedR / 2)
        LEFT_WHEEL.set_power(-forwardSpeedL / 2)
        time.sleep(0.2)
        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
    while currAngle < a - 2:
        if stopEvent.is_set():
            return
        RIGHT_WHEEL.set_power(-forwardSpeedR / 2)
        LEFT_WHEEL.set_power(forwardSpeedL / 2)
        time.sleep(0.2)
        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
        
        

            
def evade():
    global currentSquare
    global obstacleSquares
    global currAngle
    obstacleSquares[currentSquare] = True
    if (currentSquare == 1):
        if stopEvent.is_set():
            return
        straighten(veryFirstangle - 90)
        while (ultrasonicReader() < 85):
            if stopEvent.is_set():
                return
            backup(0.4)
    elif (currentSquare == 5):
        if stopEvent.is_set():
            return
        straighten(veryFirstangle + 90)
        while (ultrasonicReader() < 20):
            if stopEvent.is_set():
                return
            backup(0.3)
    elif (currentSquare == 3):
        if stopEvent.is_set():
            return
        straighten(veryFirstangle)
        while (ultrasonicReader() < 35):
            if stopEvent.is_set():
                return
            backup(0.4)
    currentSquare = 0


def home():
    global currAngle
    global angle
    while (ultrasonicReader() > 40):
        if stopEvent.is_set():
            return
        forward(0.3)
    turn90Right(currAngle)
    forward(1.2)
    while (ultrasonicReader() > 5):
        if stopEvent.is_set():
            return
        forward(0.3)
    turn90Left(currAngle)
    while (ultrasonicReader() > 5):
        if stopEvent.is_set():
            return
        forward(0.3)
    return





  
LEFT_WHEEL.set_power(0)
RIGHT_WHEEL.set_power(0)

COLOR_SENSOR_MOTOR.set_power(0)
P.set_power(0)




if __name__ == "__main__":
    gyro = threading.Thread(target=gyroReader, daemon=True)
    fireThread = threading.Thread(target=fireSiren, daemon=True)
    emergencyStopThread = threading.Thread(target=emergencyStop, daemon=True)
    emergencyStopThread.start()
    gyro.start()
    time.sleep(1)
    fireThread.start()
    straight()
    if stopEvent.is_set():
        LEFT_WHEEL.set_power(0)
        RIGHT_WHEEL.set_power(0)
        P.set_power(0)
        COLOR_SENSOR_MOTOR.set_power(0)
        exit()
    corridor()
    if stopEvent.is_set():
        LEFT_WHEEL.set_power(0)
        RIGHT_WHEEL.set_power(0)
        P.set_power(0)
        COLOR_SENSOR_MOTOR.set_power(0)
        exit()
    fullSquare()
    if stopEvent.is_set():
        LEFT_WHEEL.set_power(0)
        RIGHT_WHEEL.set_power(0)
        P.set_power(0)
        COLOR_SENSOR_MOTOR.set_power(0)
        exit()


