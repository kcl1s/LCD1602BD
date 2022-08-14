#!/usr/bin/env python3

import time
import smbus2 as smbus
BUS = smbus.SMBus(1)
### added for big digits KCL
custChar = [[31, 31, 31, 0, 0, 0, 0, 0],      # Small top line - 0
			[0, 0, 0, 0, 0, 31, 31, 31],      # Small bottom line - 1
			[31, 31, 0, 0, 0, 0, 31, 31],       # Small lines top and bottom -2
			[0, 0, 0, 0, 0, 0,  31, 31],       # Thin bottom line - 3
			[31, 31, 31, 31, 31, 31, 15, 7],  # Left bottom chamfer full - 4
			[28, 30, 31, 31, 31, 31, 31, 31], # Right top chamfer full -5
			[31, 31, 31, 31, 31, 31, 30, 28], # Right bottom chamfer full -6
			[7, 15, 31, 31, 31, 31, 31, 31]]  # Left top chamfer full -7

bigNums = [ [7, 0, 5, 4, 1, 6],         #0
			[0, 5, 254, 1, 255, 1],     #1
			[0, 2, 5, 7, 3, 1],         #2
			[0, 2, 5, 1, 3, 6],         #3
			[7, 3, 255, 254, 254, 255], #4
			[255, 2, 0, 1, 3, 6],       #5
			[7, 2, 0, 4, 3, 6],         #6
			[0, 0, 5, 254, 7, 254],     #7
			[7, 2, 5, 4, 3, 6],         #8
			[7, 2, 5, 1, 3, 6]]         #9


def write_word(addr, data):
	global BLEN
	temp = data
	if BLEN == 1:
		temp |= 0x08
	else:
		temp &= 0xF7
	BUS.write_byte(addr ,temp)

def send_command(comm):
	# Send bit7-4 firstly
	buf = comm & 0xF0
	buf |= 0x04               # RS = 0, RW = 0, EN = 1
	write_word(LCD_ADDR ,buf)
	time.sleep(0.002)
	buf &= 0xFB               # Make EN = 0
	write_word(LCD_ADDR ,buf)

	# Send bit3-0 secondly
	buf = (comm & 0x0F) << 4
	buf |= 0x04               # RS = 0, RW = 0, EN = 1
	write_word(LCD_ADDR ,buf)
	time.sleep(0.002)
	buf &= 0xFB               # Make EN = 0
	write_word(LCD_ADDR ,buf)

def send_data(data):
	# Send bit7-4 firstly
	buf = data & 0xF0
	buf |= 0x05               # RS = 1, RW = 0, EN = 1
	write_word(LCD_ADDR ,buf)
	time.sleep(0.002)
	buf &= 0xFB               # Make EN = 0
	write_word(LCD_ADDR ,buf)

	# Send bit3-0 secondly
	buf = (data & 0x0F) << 4
	buf |= 0x05               # RS = 1, RW = 0, EN = 1
	write_word(LCD_ADDR ,buf)
	time.sleep(0.002)
	buf &= 0xFB               # Make EN = 0
	write_word(LCD_ADDR ,buf)

def init(addr, bl):
#	global BUS
#	BUS = smbus.SMBus(1)
	global LCD_ADDR
	global BLEN
	global custChar	### added for big digits KCL
	LCD_ADDR = addr
	BLEN = bl
	try:
		send_command(0x33) # Must initialize to 8-line mode at first
		time.sleep(0.005)
		send_command(0x32) # Then initialize to 4-line mode
		time.sleep(0.005)
		send_command(0x28) # 2 Lines & 5*7 dots
		time.sleep(0.005)
		send_command(0x0C) # Enable display without cursor
		time.sleep(0.005)
		send_command(0x01) # Clear Screen
		BUS.write_byte(LCD_ADDR, 0x08)
		#### add custom chars for big digits KCL
		for x in range(8):
			send_command(0x40 | (x << 3))
			for i in range(8):
				send_data(custChar[x][i])
	except:
		return False
	else:
		return True

def clear():
	send_command(0x01) # Clear Screen

def openlight():  # Enable the backlight
	BUS.write_byte(0x27,0x08)
	BUS.close()

# New method for BD KCL
def bigDigit(col, digit):			# (col, digit 0-9)
	col = min(15, max(0, int(col)))		#constrain col value 0 to 15
	digit = min(9, max(0, int(digit)))	#constrain digit col value 0 to 9

	# Move cursor top row
	curPos = 0x80 + col			#same as 0x80 + 0x40 * (row = 0) + col
	send_command(curPos)
	for cc in range(0,3):
		send_data(bigNums[digit][cc])
	
	# Move cursor second row
	curPos = 0x80 + 0x40 + col	#same as 0x80 + 0x40 * (row = 1) + col
	send_command(curPos)
	for cc in range(3,6):
		send_data(bigNums[digit][cc])
	
def write(x, y, str):
	col = min(15, max(0, x))
	row = min(1, max(0, y))

	# Move cursor
	curPos = 0x80 + 0x40 * row + col
	send_command(curPos)

	for chr in str:
		send_data(ord(chr))

if __name__ == '__main__':
	init(0x27, 1)
	write(4, 0, 'Hello')
	write(4, 1, 'world!')
	for x in range(10):
		bigDigit(0,x)
		time.sleep(1)
