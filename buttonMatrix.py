#!/usr/bin/python
#
# keypad16.py
#
#

import smbus
import time

class keypad_module:

  I2CADDR    = 0x20   	# valid range is 0x20 - 0x27
  UPSIDEDOWN = 1      	# direction keypad is facing in
  PORT       = 0      	# 0 for GPIOA, 1 for GPIOB

  IODIRA = 0x00		# I/O direction register base address
  PULUPA = 0x0C		# PullUp enable register base address
  GPIOA  = 0x12		# GPIO pin register base address
  OLATA  = 0x14		# Output Latch register base address
  
  # Keypad Column output values
  KEYCOL = [0b11110111,0b11111011,0b11111101,0b11111110]

  # Keypad Keycode matrix
  KEYCODE  = [['A1','A2','A3','A4','A5','A6'], # COL0
              ['B1','B2','B3','B4','B5','B6'], # COL1
              ['C1','C2','C3','C4','C5','C6'], # COL2
              ['D1','D2','D3','D4','D5','D6'], # COL3
              ['E1','E2','E3','E4','E5','E6'], # COL4
              ['F1','F2','F3','F4','F5','F6']] # COL5

  # Decide the row
  DECODE = [0,0,0,0, 0,0,0,0, 0,0,0,1, 0,2,3,0]

  # initialize I2C comm, 1 = rev2 Pi, 0 for Rev1 Pi
  i2c = smbus.SMBus(1) 

  # get a keystroke from the keypad
  def getch(self):
    while 1:
      for col in range(0,4):
        time.sleep(0.01)
        self.i2c.write_byte_data(self.I2CADDR, self.OLATA+self.port, self.KEYCOL[col]) # write 0 to lowest four bits
        key = self.i2c.read_byte_data(self.I2CADDR, self.GPIOA+self.port) >> 4
        if (key) != 0b1111:
          row = self.DECODE[key]
          while (self.i2c.read_byte_data(self.I2CADDR, self.GPIOA+self.port) >> 4) != 15:
            time.sleep(0.01)
          if self.UPSIDEDOWN == 0:
            return self.KEYCODE[col][row] # keypad right side up
          else:
            return self.KEYCODE[3-row][3-col] # keypad upside down

  # initialize the keypad class
  def __init__(self,addr,ioport,upside):
    self.I2CADDR = addr
    self.UPSIDEDOWN = upside
    self.port = ioport
    self.i2c.write_byte_data(self.I2CADDR,self.IODIRA+self.port,0xF0) # upper 4 bits are inputs
    self.i2c.write_byte_data(self.I2CADDR,self.PULUPA+self.port,0xF0) # enable upper 4 bits pullups

# test code
def main(): 
  keypad = keypad_module(0x20,1,0)  
  while 1:
    ch = keypad.getch()
    print ch

    if ch == 'D':
      exit()

# don't runt test code if we are imported
if __name__ == '__main__':
  main()