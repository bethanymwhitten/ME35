from machine import Pin, I2C
from machine import SoftI2C
import time
from time import ticks_ms, ticks_diff
import veml6040

btn = Pin(34, Pin.IN, Pin.PULL_UP) 
DEBOUNCE_MS = 200
last_press = 0

i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)

# you can also use softI2C on regular GPIO pins
#i2c = SoftI2C(scl = Pin(33), sda = Pin(25))

print(i2c.scan())

colors = [[],[],[],[],[]]
count = 0

#importing color sensor library


# create color sensor object
sensor = veml6040.VEML6040(i2c)
#check the color sensor library on what this means
sensor.trigger_measurement()

def button_handler(pin):
    global last_press, count
    now = ticks_ms()
    if ticks_diff(now, last_press) > DEBOUNCE_MS:
        if (pin.value() == 0):
            
            last_press = now
            red, green, blue, white = sensor.read_rgbw()
            #print(red, green, blue, white)
            
            if count <= 15:
            
                if count < 5:
                    colors[4].append(1)
                    print("red")
                elif count < 10:
                    colors[4].append(2)
                    print("green")
                else:
                    colors[4].append(3)
                    print("blue")
            
                
                
                colors[0].append(red)
                colors[1].append(red)
                colors[2].append(red)
                colors[3].append(red)
                
                count +=1
                
            else:
                print(colors)
                    
                

btn.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)



