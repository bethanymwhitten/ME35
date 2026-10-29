"""
MicroPython DC motor driver for the Cytron Robo ESP32.

Motor pins (from the Robo ESP32 datasheet):
    Motor 1: M1A = GPIO12, M1B = GPIO13
    Motor 2: M2A = GPIO14, M2B = GPIO27

Each motor uses two inputs. Forward = PWM on A with B low,
reverse = PWM on B with A low. Both low = coast/stop.
Swapping the motor wires reverses which direction is "forward".
"""
from machine import Pin, PWM

M1A, M1B = 12, 13
M2A, M2B = 14, 27


class Motor:
    def __init__(self, pin_a, pin_b, freq=1000):
        self._a = PWM(Pin(pin_a), freq=freq, duty=0)
        self._b = PWM(Pin(pin_b), freq=freq, duty=0)
        self.speed = 0

    @staticmethod
    def _set(pwm, percent):
        duty = int(percent * 1023 / 100)  # 10-bit duty (0-1023)
        pwm.duty(duty)

    def run(self, speed):
        """Run motor. speed: -100 (full reverse) to +100 (full forward)."""
        speed = max(-100, min(100, speed))
        self.speed = speed
        if speed > 0:
            self._set(self._a, speed)
            self._set(self._b, 0)
        elif speed < 0:
            self._set(self._a, 0)
            self._set(self._b, -speed)
        else:
            self.stop()

    def forward(self, speed=100):
        self.run(abs(speed))

    def reverse(self, speed=100):
        self.run(-abs(speed))

    def stop(self):
        self.speed = 0
        self._set(self._a, 0)
        self._set(self._b, 0)

    def brake(self):
        """Short both terminals high to brake the motor quickly."""
        self.speed = 0
        self._set(self._a, 100)
        self._set(self._b, 100)

    def deinit(self):
        self.stop()
        self._a.deinit()
        self._b.deinit()


class RoboMotors:
    """Both motors of the Robo ESP32, with simple differential-drive helpers."""

    def __init__(self, freq=1000):
        self.m1 = Motor(M1A, M1B, freq)
        self.m2 = Motor(M2A, M2B, freq)

    def drive(self, left, right):
        """Set speeds directly (-100..100). Motor 2 = left, Motor 1 = right
        (matches Cytron's robot-car wiring examples; swap if yours differs)."""
        self.m2.run(left)
        self.m1.run(right)

    def forward(self, speed=100):
        self.drive(speed, speed)

    def backward(self, speed=100):
        self.drive(-speed, -speed)

    def turn_left(self, speed=100):
        self.drive(-speed, speed)

    def turn_right(self, speed=100):
        self.drive(speed, -speed)

    def stop(self):
        self.m1.stop()
        self.m2.stop()
