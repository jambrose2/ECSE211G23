from utils.brick import *
import time
import threading
from utils import sound

forwardSpeedR = 31
forwardSpeedL = 31
turnRadius = 0
straightDistance = 39
u = threading.Event()
distance = 500
rightDistance = 4
angle = 1000000000
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

time.sleep(1)


GYRO.reset_measure()
time.sleep(2)

note1 = sound.Sound(duration=0.2, pitch="F#4", volume=100)
note2 = sound.Sound(duration=0.2, pitch="Bb3", volume=100)

US_SENSOR_DATA_FILE = "../us_sensor.csv"
COLOR_SENSOR_DATA_FILE = "../color_sensor.csv"


stopEvent = threading.Event()


def fireSiren():
    while not stopEvent.is_set():
        note1.play()
        time.sleep(0.15)
        note2.play()
        time.sleep(0.15)
        if (stopEvent.is_set()):
            return

def ultrasonicReader():
        while not u.is_set():
            distance = US_SENSOR.get_cm()
            time.sleep(0.1)
            print("Distance: ", distance)
            return distance
            #while True:
                #distance = US_SENSOR.get_cm()
            #time.sleep
            #time.sleep(0.1)


def gyroReader():
    global angle
    global currAngle
    angle = GYRO.get_abs_measure()
    print("First", angle)
    while not stopEvent.is_set():
        currAngle = GYRO.get_abs_measure()
        time.sleep(.2)
    
def straight():
    global distance
    while True:
        LEFT_WHEEL.set_power(forwardSpeedL)
        RIGHT_WHEEL.set_power(forwardSpeedR)
        time.sleep(1.5)
        distance = ultrasonicReader()
        if distance <= straightDistance + turnRadius + 5:
            LEFT_WHEEL.set_power(0)
            RIGHT_WHEEL.set_power(0)
            #if STOP.is_set():
                #break
            turn90Right()
            return
            #straightRight()
        if distance <= straightDistance + 20:
            LEFT_WHEEL.set_power(0)
            RIGHT_WHEEL.set_power(0)
            #if STOP.is_set():
                #break
            distance = ultrasonicReader()
            for _ in range(10):
                LEFT_WHEEL.set_power(forwardSpeedL)
                RIGHT_WHEEL.set_power(forwardSpeedR)
                time.sleep(0.1)
                distance = ultrasonicReader()
                if distance <= straightDistance + turnRadius + 5:
                    LEFT_WHEEL.set_power(0)
                    RIGHT_WHEEL.set_power(0)
                    #if STOP.is_set():
                        #break
                    turn90Right()
                    return
                    #straightRight()
                    

def turn90Left(cAng):
    global currAngle
    RIGHT_WHEEL.set_power(forwardSpeedR)
    LEFT_WHEEL.set_power(-forwardSpeedL)
    time.sleep(1.3)
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)
    while currAngle > cAng + 7:
        print(currAngle)
        RIGHT_WHEEL.set_power(forwardSpeedR/2)
        time.sleep(0.1)
    RIGHT_WHEEL.set_power(0)

def turn90Right(cAng):
    global currAngle
    RIGHT_WHEEL.set_power(-forwardSpeedR)
    LEFT_WHEEL.set_power(forwardSpeedL)
    time.sleep(1.3)
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)
    while currAngle < cAng - 7:
        print(currAngle)
        RIGHT_WHEEL.set_power(forwardSpeedR/2)
        time.sleep(0.1)
    RIGHT_WHEEL.set_power(0)

def corridor():
    distance = ultrasonicReader()
    while distance > rightDistance + 20:
        LEFT_WHEEL.set_power(forwardSpeedL)
        RIGHT_WHEEL.set_power(forwardSpeedR)
        time.sleep(.5)
        distance = ultrasonicReader()
    if distance <= rightDistance + turnRadius:
        distance = ultrasonicReader()
        if distance <= rightDistance + turnRadius:
            LEFT_WHEEL.set_power(0)
            RIGHT_WHEEL.set_power(0)
            turn90Left()
        distance = ultrasonicReader()
    if distance <= rightDistance + 20: 
        LEFT_WHEEL.set_power(0)
        RIGHT_WHEEL.set_power(0)
        for _ in range(10):
            distance = ultrasonicReader()
            LEFT_WHEEL.set_power(forwardSpeedL)
            RIGHT_WHEEL.set_power(forwardSpeedR)
            time.sleep(0.1)
            if distance <= rightDistance + turnRadius + 5:
                if distance <= rightDistance + turnRadius + 5:
                    LEFT_WHEEL.set_power(0)
                    RIGHT_WHEEL.set_power(0)
            turn90Left(angle)
            forward(1)
            time.sleep(1.5)
            stopEvent.set()
            fullSquare()

def turn180():
    RIGHT_WHEEL.set_power(forwardSpeedR)
    LEFT_WHEEL.set_power(-forwardSpeedL)
    time.sleep(1.5)
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)


    
def backup(dist):
    RIGHT_WHEEL.set_power(-forwardSpeedR)
    LEFT_WHEEL.set_power(-forwardSpeedL)
    time.sleep(dist)
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)
    
def get_color():
    color = COLOR_SENSOR.get_rgb()
    i = colorIdentifier(color)
    return i
            
def colorIdentifier(rgb):
    if rgb[0] == None or rgb[1] == None or rgb[2] == None:
        return 0
    s = rgb[0] + rgb[1] + rgb[2]
    if (s < 150):
        return 3
    newRGB = [rgb[0]/s, rgb[1]/s, rgb[2]/s]
    if newRGB[0] > 0.6:
        if newRGB[1] < 0.4:
            if newRGB[2] < 0.3:
                if rgb[1] < 55:
                    return 0
                print(rgb)
                return 1
    elif newRGB[0] < 0.37:
        if newRGB[1] > 0.55:
            if newRGB[2] < 0.1:
                return 2
    else:
        print("Unable to Identify")
        return 0
    
def extinguishProtocol():
    global currentSquare
    global fireSquares
    fireSquares[currentSquare] = True
    print("ext")
    RIGHT_WHEEL.set_power(forwardSpeedR / 2)
    time.sleep(0.25)
    COLOR_SENSOR_MOTOR.set_position_relative(90)
    time.sleep(1)
    backup(2)
    COLOR_SENSOR_MOTOR.set_position_relative(-90)
    time.sleep(2)
    time.sleep(0.5)
    P.set_power(-50)
    time.sleep(1)
    P.set_power(0)
    RIGHT_WHEEL.set_power(-forwardSpeedR / 2)
    time.sleep(0.25)
    forward(2)
    firesPutOut += 1
    if firesPutOut == 2:
        stopEvent.set()
        return

    
def backup(length):
    RIGHT_WHEEL.set_power(-20)
    LEFT_WHEEL.set_power(-20)
    time.sleep(length)
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)
    
def forward(length):
    RIGHT_WHEEL.set_power(20)
    LEFT_WHEEL.set_power(20)
    time.sleep(length - 0.2)
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)

    
def fireFind():
    global currAngle
    global currentSquare
    color = 0
    color2 = 0
    for i in range(150):
        RIGHT_WHEEL.set_power(forwardSpeedR * 0.5)
        LEFT_WHEEL.set_power(-forwardSpeedL * 0.5)
        time.sleep(.1)
        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
        color = get_color()
        print("1: ", color)
        if (color == 3):
            break
        if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
            elif (color2 == 2):
                evade()
    while (currAngle > angle + 5):
        print(currAngle)
        RIGHT_WHEEL.set_power(forwardSpeedR * 0.5)
        LEFT_WHEEL.set_power(-forwardSpeedL * 0.5)
        time.sleep(.1)
    LEFT_WHEEL.set_power(forwardSpeedL * 0.5)
    RIGHT_WHEEL.set_power(-forwardSpeedR * 0.5)
    time.sleep(0.5)
    for i in range(150):
        if currentSquare == 3:
            if i > 2:
                if (ultrasonicReader() < 2):
                    backup(0.3)
                    straighten(angle)
                    while (ultrasonicReader() < 32):
                        backup(0.4)
        LEFT_WHEEL.set_power(forwardSpeedL * 0.5)
        RIGHT_WHEEL.set_power(-forwardSpeedR * 0.5)
        time.sleep(0.1)
        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
        color = get_color()
        if (color == 3):
            break
        print("1: ", color)
        if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
            elif (color2 == 2):
                evade()
    while (currAngle < angle - 5):
        print(currAngle)
        RIGHT_WHEEL.set_power(forwardSpeedR * 0.5)
        LEFT_WHEEL.set_power(-forwardSpeedL * 0.5)
        time.sleep(.15)
    for _ in range(22):
        if (currAngle > angle + 5):
            RIGHT_WHEEL.set_power(forwardSpeedR * 0.5)
            LEFT_WHEEL.set_power(-forwardSpeedL * 0.5)
            time.sleep(.15)
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
        else:
            break
    if currentSquare == 3 or currentSquare == 5 or currentSquare == 2 or currentSquare == 4:
        if (ultrasonicReader() < 4):
            backup(0.3)
            straighten(angle)
            while (ultrasonicReader() < 32):
                    backup(0.4)
    GYRO.reset_measure()
    time.sleep(1.5)
    
def fullSquare():
    global currAngle
    global currentSquare
    visited[currentSquare] = True
    #
    #  Square 0
    while (ultrasonicReader() < 35):
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
    forward(0.4)
    time.sleep(1)
    for _ in range(5):
        fireFind()
        forward(0.4)
        color = get_color()
        if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
    if (currAngle < angle - 5):
        for _ in range(20):
            RIGHT_WHEEL.set_power(forwardSpeedR * 0.5)
            LEFT_WHEEL.set_power(-forwardSpeedL * 0.5)
            time.sleep(.15)
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            if (get_color == 3):
                break
    if (currAngle > angle + 5):
        for _ in range(20):
            RIGHT_WHEEL.set_power(-forwardSpeedR * 0.5)
            LEFT_WHEEL.set_power(forwardSpeedL * 0.5)
            time.sleep(.15)
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            if (get_color == 3):
                break
    forward(1)
    backup(0.5)
    time.sleep(1)
    currentSquare = 3
    visited[currentSquare] = True
    color = get_color()
    #
    # Back middle square
    if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
            elif (color2 == 2):
                evade()
    forward(0.65)
    time.sleep(1)
    for _ in range(5):
        fireFind()
        forward(0.4)
        color = get_color()
        if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
    while (ultrasonicReader() < 20):
        backup(0.4)
    turn90Left()
    while (ultrasonicReader() > 85):
        forward(0.4)
    time.sleep(1)
    currentSquare = 1
    visited[currentSquare] = True
    color = get_color()
    #
    # Front left square
    if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
            elif (color2 == 2):
                evade()
    forward(0.65)
    time.sleep(1)
    for _ in range(5):
        fireFind()
        forward(0.65)
        color = get_color()
        if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
            elif (color2 == 2):
                evade()
    #
    # Back left square
    if obstacleSquares[1] == False:
        straighten(angle - 90)
        while (ultrasonicReader() < 65):
            backup(0.4)
        turn90Right()
        while (ultrasonicReader() < 20):
            forward(0.3)
        currentSquare = 2
        visited[currentSquare] = True
        color = get_color()
        if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
            elif (color2 == 2):
                evade()
        forward(0.65)
        time.sleep(1)
        for _ in range(5):
            fireFind()
            forward(0.65)
            color = get_color()
            if (color == 1 or color == 2):
                color2 = get_color()
                print("2: ", color2)
                if (color2 == 1):
                    print("ext proto")
                    extinguishProtocol()
                elif (color2 == 2):
                    evade()
        straighten(angle)
        while (ultrasonicReader() < 20):
            backup(0.4)
        turn90Right(currentAngle)
        while (ultrasonicReader() < 20):
            forward(0.4)
    else:
        turn180()
        while (ultrasonicReader() < 20):
            forward(0.4)
    currentSquare = 5
    visited[currentSquare] = True
    color = get_color()
    #
    # Front right square
    if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
            elif (color2 == 2):
                evade()
    forward(0.65)
    time.sleep(1)
    for _ in range(5):
        fireFind()
        forward(0.65)
        color = get_color()
        if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
            elif (color2 == 2):
                evade()
    #
    # Back right square
    if (obstacleSquares[5] == False):
        straighten(angle + 90)
        while (ultrasonicReader() < 4):
            backup(0.4)
        while (ultrasonicReader() > 4):
            forward(0.4)
        turn90Left(currAngle)
        while (ultrasonicReader() > 20):
            forward(0.4)
        currentSquare = 4
        visited[currentSquare] = True
        if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
            elif (color2 == 2):
                evade()
        forward(0.65)
        time.sleep(1)
        for _ in range(5):
            fireFind()
            forward(0.65)
            color = get_color()
            if (color == 1 or color == 2):
                color2 = get_color()
                print("2: ", color2)
                if (color2 == 1):
                    print("ext proto")
                    extinguishProtocol()
                elif (color2 == 2):
                    evade()
        straighten(angle)
        while (ultrasonicReader() < 20):
            backup(0.4)
        turn90Left(currAngle)
        while (ultrasonicReader() > 90):
            forward(0.4)
        #
        # Go home if all done
        if (visited[1] == True):
            turn90Right(currAngle)
            home()
            return
        #
        # Search top left from other angle
        else:
            if (obstacleSquares[3] == False):
                while (ultrasonicReader() > 85):
                    forward(0.4)
                currentSquare = 1
                visited[currentSquare] = True
                color = get_color()
                if (color == 1 or color == 2):
                    color2 = get_color()
                    print("2: ", color2)
                    if (color2 == 1):
                        print("ext proto")
                        extinguishProtocol()
                    elif (color2 == 2):
                        evade()
                forward(0.65)
                time.sleep(1)
                for _ in range(5):
                    fireFind()
                    forward(0.65)
                    color = get_color()
                    if (color == 1 or color == 2):
                        color2 = get_color()
                        print("2: ", color2)
                        if (color2 == 1):
                            print("ext proto")
                            extinguishProtocol()
                        elif (color2 == 2):
                            evade()
                straighten(angle + 90)
                
    else:
        while (ultrasonicReader() < 20):
            backup(0.4)
        currentSquare = 0
        turn90Left(currAngle)
        time.sleep(1)

    if (visited[4] == False):
        while (ultrasonicReader() > 4):
            forward(0.4)
        turn90Right(currAngle)
        while (ultrasonicReader() > 20):
            forward(0.4)
        currentSquare = 4
        visited[currentSquare] = True
        color = get_color()
        if (color == 1 or color == 2):
            color2 = get_color()
            print("2: ", color2)
            if (color2 == 1):
                print("ext proto")
                extinguishProtocol()
            elif (color2 == 2):
                evade()
        forward(0.65)
        time.sleep(1)
        for _ in range(5):
            fireFind()
            forward(0.65)
            color = get_color()
            if (color == 1 or color == 2):
                color2 = get_color()
                print("2: ", color2)
                if (color2 == 1):
                    print("ext proto")
                    extinguishProtocol()
                elif (color2 == 2):
                    evade()
        turn180()
        while (ultrasonicReader() < 20):
            forward(0.4)
        if (visited[1] == True):
            turn90Left(currAngle)
            home()
        else:
            while (ultrasonicReader() > 85):
                forward(0.4)
            
        


    
    
    

    
    
    
def straighten(a):
    global currAngle
    while currAngle > a + 5:
        RIGHT_WHEEL.set_power(forwardSpeedR / 2)
        LEFT_WHEEL.set_power(-forwardSpeedL / 2)
        time.sleep(0.2)
        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
    while currAngle < a - 5:
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
        straighten(angle - 90)
        while (ultrasonicReader() < 85):
            backup(0.4)
    elif (currentSquare == 5):
        straighten(angle + 90)
        while (ultrasonicReader() < 20):
            backup(0.3)
    elif (currentSquare == 3):
        straighten(0)
        while (ultrasonicReader() < 35):
            backup(0.4)
    elif (currentSquare == 2):
        if (obstacleSquares[1] == False):
            straighten(angle - 90)
            while (ultrasonicReader() < 22):
                backup(0.4)
            turn90Right()
            while (ultrasonicReader() < 20):
                forward(0.3)
    
    currentSquare = 0






  
LEFT_WHEEL.set_power(0)
RIGHT_WHEEL.set_power(0)

COLOR_SENSOR_MOTOR.set_power(0)
P.set_power(0)


#extinguishProtocol()
#extinguishProtocol()
#fireThread = threading.Thread(target=fireSiren, daemon=True)
#fireThread.start()
gyro = threading.Thread(target=gyroReader, daemon=True)
gyro.start()
#straight()
#corridor()
fullSquare()



