from encoder import Motor
from machine import Pin

Motor1 = Motor(12,13, 32,39) 
Motor1.pos()

DEBOUNCE_MS = 200
last_press = 0
pressed_flag = False

trainData = [0, 0]
trainingCount = 0

encButton = Pin(34, Pin.IN, Pin.PULL_UP)

def encButton(p):
    if (encButton.value() == 0):
        last_press = now
        print("Button pressed!")
        count +=1
        print(count)
    
encButton.irq(trigger=Pin.IRQ_RISING, handler=encButton)

while True:
    if pressed_flag:
        if trainingCount < len(trainData):
            print("train")
            