import neopixel
import time
from machine import Pin
print("start")
lights = neopixel.NeoPixel(Pin(15),2)

rainbow = [(20, 0, 0),
           (20, 5, 0),
           (20, 20, 0),
           (0, 20, 0),
           (0, 0, 20),
           (5, 0, 10),
           (10, 10, 10)]

while True:
        for i in range(0, len(rainbow)):
            lights[0] = lights[1] = rainbow[i]
            lights.write()
            time.sleep(.5)

lights.write()
print("done")