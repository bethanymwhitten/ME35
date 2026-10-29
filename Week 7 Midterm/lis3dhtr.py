"""
MicroPython driver for the LIS3DHTR 3-axis accelerometer (I2C).
Tested design target: ESP32. Works on any port with machine.I2C.

I2C address: 0x18 (SDO/SA0 = GND) or 0x19 (SDO/SA0 = VCC, Grove default).
"""
import struct
from time import sleep_ms

# Registers
_WHO_AM_I = 0x0F
_CTRL_REG1 = 0x20
_CTRL_REG4 = 0x23
_STATUS_REG = 0x27
_OUT_X_L = 0x28

_DEVICE_ID = 0x33

# Output data rates (CTRL_REG1 ODR[3:0])
RATE_POWER_DOWN = 0x0
RATE_1HZ = 0x1
RATE_10HZ = 0x2
RATE_25HZ = 0x3
RATE_50HZ = 0x4
RATE_100HZ = 0x5
RATE_200HZ = 0x6
RATE_400HZ = 0x7

# Full-scale ranges (CTRL_REG4 FS[1:0])
RANGE_2G = 0
RANGE_4G = 1
RANGE_8G = 2
RANGE_16G = 3

_RANGE_G = {RANGE_2G: 2, RANGE_4G: 4, RANGE_8G: 8, RANGE_16G: 16}

GRAVITY = 9.80665  # m/s^2


class LIS3DHTR:
    def __init__(self, i2c, address=0x19, rate=RATE_100HZ, range_=RANGE_2G,
                 high_res=True):
        self.i2c = i2c
        self.addr = address
        self._range = range_
        self._high_res = high_res
        self._buf = bytearray(6)

        if self.device_id() != _DEVICE_ID:
            raise OSError("LIS3DHTR not found at 0x%02X (WHO_AM_I=0x%02X)"
                          % (address, self.device_id()))

        self.set_rate(rate)
        self.set_range(range_)

    # ---- low-level helpers ----
    def _read(self, reg, n=1):
        return self.i2c.readfrom_mem(self.addr, reg, n)

    def _write(self, reg, value):
        self.i2c.writeto_mem(self.addr, reg, bytes([value]))

    # ---- configuration ----
    def device_id(self):
        return self._read(_WHO_AM_I)[0]

    def set_rate(self, rate):
        """Set output data rate; enables X/Y/Z axes. Use RATE_POWER_DOWN to sleep."""
        self._rate = rate
        self._write(_CTRL_REG1, (rate << 4) | 0x07)  # XYZ enabled, normal/HR mode
        sleep_ms(10)

    def set_range(self, range_):
        """Set full-scale range: RANGE_2G/4G/8G/16G."""
        self._range = range_
        # BDU=1 (block data update), FS bits, HR bit
        value = 0x80 | (range_ << 4) | (0x08 if self._high_res else 0x00)
        self._write(_CTRL_REG4, value)
        sleep_ms(10)

    def power_down(self):
        self.set_rate(RATE_POWER_DOWN)

    # ---- data ----
    def data_ready(self):
        """True when a new XYZ sample is available."""
        return bool(self._read(_STATUS_REG)[0] & 0x08)

    def read_raw(self):
        """Return raw signed 16-bit (left-justified) x, y, z."""
        # Bit 7 of the register address enables address auto-increment
        self.i2c.readfrom_mem_into(self.addr, _OUT_X_L | 0x80, self._buf)
        return struct.unpack("<hhh", self._buf)

    def read_g(self):
        """Return acceleration (x, y, z) in g."""
        scale = _RANGE_G[self._range] / 32768.0
        x, y, z = self.read_raw()
        return x * scale, y * scale, z * scale

    def read_ms2(self):
        """Return acceleration (x, y, z) in m/s^2."""
        x, y, z = self.read_g()
        return x * GRAVITY, y * GRAVITY, z * GRAVITY
