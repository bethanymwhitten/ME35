from machine import I2C, Pin, PWM
import time
import lis3dhtr, math

servo = PWM(Pin(4), freq=50, duty_u16=0)
servoLimOpen = 1.6
servoLimClosed = 0.5


servo.duty_u16(int(1.6*65535/20))
time.sleep(2)

servo.duty_u16(int(0.5*65535/20))
time.sleep(0.25)


servo.duty_u16(int(1.6*65535/20))
time.sleep(2.5)

servo.duty_u16(int(0.5*65535/20))
time.sleep(0.25)


servo.duty_u16(int(1.6*65535/20))