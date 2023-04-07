"""

DC Solar driven load controller.

"""
import math
import time
from machine import Pin, I2C, ADC, SPI
import ujson
import tm1637
from boot import network_up
from neopixel import NeoPixel
from provision import provision, CHIP_OFF, CHIP_LOW, CHIP_NOMINAL, CHIP_HIGH

LOW_POWER = (0,0,255)


CHIPS_NUM = 195

# APW9+_14.5V-21V
V_ULTRA_LOW = 12.1
V_NOMINAL = 14.5
V_MAX = 21

# define 4 digit display, flash everything
tm = tm1637.TM1637(clk=Pin(21), dio=Pin(19))
tm.numbers(88, 88, True)

pixels = NeoPixel(Pin(15), CHIPS_NUM)


led = Pin(12, Pin.OUT)
pot = Pin(35, Pin.IN)
pot_a = ADC(pot)  

"""
Boot sequence 
"""

# bring up wifi   
network_up(tm)

chip_state = [0]*CHIPS_NUM


def get_voltage(pot_a, chip_state):
  vin_uv = pot_a.read_u16()
  vin_frac = vin_uv/65535
  vin = V_ULTRA_LOW + vin_frac*(V_MAX-V_ULTRA_LOW)

  # subtract a simulated voltage drop
  load = len([state for i,state in enumerate(chip_state) if state == CHIP_LOW])
  simulated_drop  = load*0.01
  print(str(simulated_drop) + " drop")
  return vin-simulated_drop

while True:

  # read voltage
  v = get_voltage(pot_a, chip_state) 
  print(str(v) + " voltage")

  # print the voltage
  tm.numbers(math.floor(v), int((v%1)*100))
  led.value(v)

  # provision chips
  chip_state = provision(chip_state, v, V_ULTRA_LOW, V_NOMINAL, V_MAX)

  # display state
  for i in range(CHIPS_NUM):
      if  chip_state[i] == CHIP_OFF:  
        pixels[i] = (0,0,0,10)
      elif  chip_state[i] == CHIP_LOW:  
        pixels[i] = (0,0,255)
      elif  chip_state[i] == CHIP_NOMINAL:  
        pixels[i] = (0,255,0)
      elif  chip_state[i] == CHIP_HIGH:
        pixels[i] = (255,0,0)
      else:
        pixels[i] = (0,0,0)

  pixels.write()

  time.sleep(1)

