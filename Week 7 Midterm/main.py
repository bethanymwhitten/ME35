from machine import I2C, Pin, PWM
from time import sleep_ms
import lis3dhtr, math
from robo_motor import RoboMotors
import time

motors = RoboMotors()

# ---- Settings you can tune ----
loop_ms = 20 # loop period (50 Hz update)
openTime = 2.0 # time to open fully while moving
closeTime = 8.0 # time to close fully when still (slower than opening)
moveThreshold = 0.015 # change between samples that counts as "moved"

countToCandy = 200
count = 0

servoOpen_ms = 1.6 # pulse width (ms) for open
servoClosedn_ms = 0.5 # pulse width (ms) for closed

# ---- Hardware ----
i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)
print("I2C devices:", [hex(a) for a in i2c.scan()])

accel = lis3dhtr.LIS3DHTR(i2c, address=0x19,
                          rate=lis3dhtr.RATE_100HZ,
                          range_=lis3dhtr.RANGE_4G)

servo = PWM(Pin(4), freq=50)


def set_servo(pulse_ms):
    # 50 Hz -> 20 ms period
    servo.duty_u16(int(pulse_ms * 65535 / 20))


# Per-loop step sizes derived from the open/close times
span = servoOpen_ms - servoClosedn_ms
open_step = span / (openTime * 1000 / loop_ms)
close_step = span / (closeTime * 1000 / loop_ms)

pos = servoClosedn_ms
set_servo(pos)

xl, yl, zl = accel.read_g()

while True:
    x, y, z = accel.read_g()

    # Size of the change since the last sample (gravity cancels out)
    delta = math.sqrt((x - xl) ** 2 + (y - yl) ** 2 + (z - zl) ** 2)
    xl, yl, zl = x, y, z

    if delta > moveThreshold:
        pos = min(servoOpen_ms, pos + open_step) # open
        count = count + 1
        print(count)
        if count > countToCandy:
            motors.m1.run(40)
            time.sleep(.25)
            motors.m1.stop()
            count = 0
            
    else:
        pos = max(servoClosedn_ms, pos - close_step) # close (slower)
        count = 0

    set_servo(pos)
    sleep_ms(loop_ms)
