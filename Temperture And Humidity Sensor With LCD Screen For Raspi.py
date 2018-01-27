import smbus
import time
import dht11
import RPI.GPIO as GPIO

#define GPIO 14 as DHT11 data pin
Temp_sensor=14

# define some devise parameters
I2C_ADDR = 0x3f # I2C devise address, if any error, change this address to
LCD_WIDTH = 16  # maximum charecters per line

# define some devise constants
LCD_CHR = 1  # Mode - sending data
LCD_CMD = 0  # Mode - sending command

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xCO
LCD_LINE_3 = 0x94
LCD_LINE_4 = 0xD4

LCD BACKLIGHT = 0x08


ENABLE = 0b00000100


E_PULSE = 0.0005
E_DELAY = 0.0005


#bus = smbus.SMBus(0)   # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def lcd_init():
    #initialize display
    lcd_byte(0x33,LCD_CMD)
    lcd_byte(0x32,LCD_CMD)
    lcd_byte(0x06,LCD_CMD)
    lcd_byte(0x0C,LCD_CMD)
    lcd_byte(0x28,LCD_CMD)
    lcd_byte(0x01,LCD_CMD)
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    # send byte to data pins
    # bits = the data
    # mode = 1 for data
    #        0 for command

    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

    # high bits
    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    #low bits
    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)

 def lcd_toggle_enable(bits):
    # toggle enable
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
    time.sleep(E_DELAY)

def lcd_string(message,line):
    # send string to display

    message = message.ljust(LCD_WIDTH," ")

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)

def main():
    # main prgram block\
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)      #use BCM GPIO numbers
    # Initialize display
    lcd_init()
    instance = dht11.DHT11(pin = Temp_sensor)

    while True:
        #get DHT11 sensor value
        result = instance.read()
        # send some test

        if result.is_valid():
            lcd_string("temp:"+str(result))
            lcd_string("humid:"+str(result.humidity)+"%",LCD_LINE_2)
            lcd_sleep(3) # 3 second delay
            lcd_string("Read Tutorial:",LCD_LINE_1)
            lcd_string("osoyoo.com",LCD_LINE_2)
            time.sleep(3)

if__name__ == '__main__':

  try:
    main()
except KeyboardInterupt:
    pass
finally:    
    lcd_byte(0x01, LCD_CMD)
