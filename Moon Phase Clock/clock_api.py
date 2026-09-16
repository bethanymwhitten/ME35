#importing the libraries
import network
import urequests
import time
from time import ticks_ms, ticks_diff
import requests
from machine import PWM, Pin
import secrets

#setting up SSID and password

SSID = "tufts_eecs" #use tufts_eecs
PASSWORD = "foundedin1883" #foundedin1883

# SSID = "Tibbetts"
# PASSWORD = "georgest42"

SSID = "Tufts_Wireless"

minute_hand = PWM(Pin(4), freq=50, duty_u16=0)
hour_hand  = PWM(Pin(18), freq=50, duty_u16=0)

led_1 = Pin(16, Pin.OUT)
led_2 = Pin(17, Pin.OUT)

btn = Pin(25, Pin.IN, Pin.PULL_UP)
DEBOUNCE_MS = 200
last_press = 0

mode_changed = False

global MODE_TIME

#function definition
def connect_wifi():
    import secrets
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(SSID)
        while not wlan.isconnected():
            time.sleep(0.5)
    print("Connected! IP address:", wlan.ifconfig()[0])
    return wlan

def read_time():
    import secrets

    response = requests.get(secrets.time_url, headers=secrets.time_headers)

    time_full = response.json()

#     print(time_full['datetime'])

    time_split = time_full['datetime'].split('T')
    time_split[0] = time_split[0].strip('T')
    time_split[1] = time_split[1].split('-')
    time_split[1] = time_split[1][0]
#     print(time_split)

    date = time_split[0]
    clock_time = time_split[1].split(':')
    response.close()
    return date, clock_time

def read_moon():
    date, clock_time = read_time()

    url = "https://aa.usno.navy.mil/api/rstt/oneday?date="+date+"&coords=42.42,-71.12"

    response = requests.get(url)
    phase = response.json()

    current_phase = phase['properties']['data']['curphase']

    response.close()

    print(current_phase)

    return current_phase

def button_handler(pin):
    global last_press
    global MODE_TIME
    global mode_changed
    now = ticks_ms()
    if ticks_diff(now, last_press) > DEBOUNCE_MS:
        if (pin.value() == 0):
            last_press = now
            MODE_TIME = not MODE_TIME
            mode_changed = True
            print("Toggled")

def interruptible_sleep(ms):
    global mode_changed
    start = ticks_ms()
    while ticks_diff(ticks_ms(), start) < ms:
        if mode_changed:
            mode_changed = False
            print("Interupted")
            return True
        time.sleep_ms(20)
    return False

btn.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)


#function call
connect_wifi()

# date, clock_time = read_time()
# current_phase = read_moon()
# print(current_phase)


# SERVO POS DEFNINITION
SERVO_MAX = 2500*1000
SERVO_MIN = 500*1000 #placeholders
SERVO_SCALE = SERVO_MAX-SERVO_MIN

MODE_TIME = True

while True:
    print(MODE_TIME)
    if MODE_TIME:
        # CLOCK MODE
        led_1.value(0)
        led_2.value(0)
        date, clock_time = read_time()
        minute_pos = ((int(clock_time[1])/60) * SERVO_SCALE) + SERVO_MIN + 250
        hour_pos = (((int(clock_time[0])%12)/12)*SERVO_SCALE)+SERVO_MIN + (minute_pos-SERVO_MIN)/12
        print("Minute_Pos: " + str(minute_pos))
        print("Hour_Pos: " + str(hour_pos))
        minute_hand.duty_ns(int(minute_pos))
        time.sleep_ms(1000)
        hour_hand.duty_ns(int(hour_pos))
        interruptible_sleep(60*1000)

    else:
        # MOON MODE
        phase = read_moon()
        print("Moon Mode")
        led_1.value(1)
        led_2.value(1)
#         phase = "Waning Crescent"
        if phase == "New Moon":
            minute_hand.duty_ns(1300*1000)
            time.sleep_ms(1000)
            hour_hand.duty_ns(1500*1000)
        elif phase == "Waxing Crescent":
            minute_hand.duty_ns(1250*1000)
            time.sleep_ms(1000)
            hour_hand.duty_ns(1000*1000)
        elif phase == "First Quarter":
            minute_hand.duty_ns(1800*1000)
            time.sleep_ms(1000)
            hour_hand.duty_ns(1500*1000)
        elif phase == "Waxing Gibbous":
            minute_hand.duty_ns(1250*1000)
            time.sleep_ms(1000)
            hour_hand.duty_ns(1000*1000)
        elif phase == "Full Moon":
            minute_hand.duty_ns(2000*1000)
            time.sleep_ms(1000)
            hour_hand.duty_ns(1000*1000)
        elif phase == "Waning Gibbous":
            minute_hand.duty_ns(2000*1000)
            time.sleep_ms(1000)
            hour_hand.duty_ns(1700*1000)
        elif phase == "Last Quarter":
            minute_hand.duty_ns(1300*1000)
            time.sleep_ms(1000)
            hour_hand.duty_ns(1000*1000)
        elif phase == "Waning Crescent":
            minute_hand.duty_ns(2000*1000)
            time.sleep_ms(1000)
            hour_hand.duty_ns(1650*1000)

        interruptible_sleep(60*60*1000) #1h sleep since moon phase doesn't update quickly