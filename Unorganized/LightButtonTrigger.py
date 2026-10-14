import neopixel
from machine import Pin
from time import ticks_ms, ticks_diff

btn = Pin(34, Pin.IN, Pin.PULL_UP) 
DEBOUNCE_MS = 200
last_press = 0
lights = neopixel.NeoPixel(Pin(15), 2)
rainbow = [(20, 0, 0),
           (20, 5, 0),
           (20, 20, 0),
           (0, 20, 0),
           (0, 0, 20),
           (5, 0, 10),
           (10, 10, 10)]
count = 0
lights[0] = lights[1] = rainbow[count]
lights.write()


def button_handler(pin):
    global last_press, count, rainbow, lights
    now = ticks_ms()
    if ticks_diff(now, last_press) > DEBOUNCE_MS:
        if (pin.value() == 0):
            last_press = now
            print("Button pressed!")
            count +=1
            print(count)
            if count >= len(rainbow):
                count = 0
            lights[0] = lights[1] = rainbow[count]
            lights.write()

btn.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)