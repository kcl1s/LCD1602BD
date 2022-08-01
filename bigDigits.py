import time
import LCD1602BD as lcd

def bigFloat(value):  # custom function to use whole display for a float number with tenths precision
    lcd.clear()
    curPlace=13                             # start with cursor for least significant digit
    lcd.write(12,1,'\x2e')                  # place large decimal point so one digit to right
    valAsInt=round(value * 10)              # time 10 and round so we are working in integers
    valAsInt=min(9999,max(-9999,valAsInt))  # constrain 4 digits positive or negative
    if valAsInt < 0:                        # check for negative value
        negVal = True
        valAsInt = abs(valAsInt)
    else:
        negVal = False
    while (valAsInt >= 10):                 # work through digits right to left
        lcd.bigDigit(curPlace,(valAsInt % 10))
        valAsInt = valAsInt // 10
        curPlace -= 4                       # move cursor to next digit
    lcd.bigDigit(curPlace,valAsInt)         # place most siginificant digit when valAsInt < 10 
    if (negVal):
        lcd.write(curPlace-1,0,'\x03')      # place minus sign if needed

lcd.init(0x27, 1)

for x in range(0,100):
    tens= int(x / 10)
    ones= int(x % 10)
    lcd.bigDigit(0,tens)
    lcd.bigDigit(4,ones)
    time.sleep(.2)

bigFloat(-35.27)   
