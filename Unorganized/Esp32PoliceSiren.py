import neopixel
import time
from machine import Pin, PWM
print("start")
lights = neopixel.NeoPixel(Pin(15), 2)
buzzer = PWM(Pin(23))
color = [(20, 0, 0),
         (0, 0, 20)]

buzzer.duty(10)

while True:
    
    buzzer.freq(200)
    lights[0] = color[1]
    lights[1] = color[0]
    lights.write()
    time.sleep(.5)
    
    buzzer.freq(400)
    lights[0] = color[0]
    lights[1] = color[1]
    lights.write()
    time.sleep(.5)
