import numpy as np
import matplotlib.pyplot as plt
import math

# original point
cx = 3
cy = 4

# point being rotated
x = 10
y = 11

# rotation movement
theta = math.sqrt(3)/2 #60deg



def rotate_around_point(x, y, cx, cy, theta):
    
    # Translate to origin
    x = x - cx
    y = y - cy
    
    # Rotate
    
    theta0 = math.tan(y/x)
    theta1 = theta0 + theta
    L = math.sqrt(x*x + y*y)
    
    x = L*math.cos(theta1)
    y = L*math.sin(theta1)
    
    # Translate back
    x_final = x + cx
    y_final = y + cy
    
    print(x_final) #0.43
    print(y_final) #13.56
    
    return x_final, y_final

rotate_around_point(x, y, cx, cy, theta)