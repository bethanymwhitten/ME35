import neopixel
from machine import Pin
print("start")
lights = neopixel.NeoPixel(Pin(15),2)

color1 = [20, 20, 0]
thres = 20
while True:
    if color1(1) > thres && color1(1) >= 0
        color1 = [color1(1) - 1, color1(2), color1(3)]
    lights[0] = color1
    lights[1] = [0,0,20]

lights.write()
print("done")