from machine import ADC, Pin
from time import ticks_diff, ticks_ms

lightsensor = ADC(Pin(39))

btn1 = Pin(34, Pin.IN, Pin.PULL_UP)
btn2 = Pin(35, Pin.IN, Pin.PULL_UP) 
DEBOUNCE_MS = 200
last_press = 0

pressed_flag = False

data = [[],[]]
count = 1

def button_handler1(pin):
    global last_press
    global pressed_flag
    now = ticks_ms()
    if ticks_diff(now, last_press) > DEBOUNCE_MS:
        if (pin.value() == 0):
            last_press = now
            pressed_flag = True
            
def button_handler2(pin):
    global last_press, data
    global pressed_flag
    now = ticks_ms()
    if ticks_diff(now, last_press) > DEBOUNCE_MS:
        if (pin.value() == 0):
            last_press = now
            #pressed_flag = True
            print(data)

btn1.irq(trigger=Pin.IRQ_FALLING, handler=button_handler1)
btn2.irq(trigger=Pin.IRQ_FALLING, handler=button_handler2)

while True:
    if pressed_flag:
        data[0].append(count)
        data[1].append(lightsensor.read_u16())
        #print(data)
        pressed_flag = False
        count +=1
