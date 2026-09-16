import encoder
import time

from machine import PWM, Pin
servo1 = PWM(Pin(4), freq=50, duty_u16=0)
servo2 = PWM(Pin(5), freq=50, duty_u16=0)
# or from encoder import Count
count = encoder.Count(21,22)
count2 = encoder.Count(25,26)
# or count = Count(32,39)

while True:
    print(count.value())
    encoderBaseVal = ((count.value() + 1000)/1000) + 0.5
    encoderArmVal = ((count2.value() + 480)/480) + 0.5
    time.sleep(0.1)
    if encoderBaseVal > 2.5:
        encoderBaseVal = 2.5
    elif encoderBaseVal < .5:
        encoderBaseVal = .5

    if encoderArmVal > 2.5:
        encoderArmVal = 2.5
    elif encoderArmVal < .5:
        encoderArmVal = .5


    servo1.duty_u16(int(encoderBaseVal*65535 /20))
    servo2.duty_u16(int(encoderArmVal*65535/20))