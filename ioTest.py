import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import time

pin0 = 11
pin1 = 5
pin2 = 6
pin3 = 13
pin4 = 19
pin5 = 26

GPIO.setup(pin0,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin3,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin4,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin5,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

while True:
    b0 = GPIO.input(pin0)
    b1 = GPIO.input(pin1)
    b2 = GPIO.input(pin2)
    b3 = GPIO.input(pin3)
    b4 = GPIO.input(pin4)
    b5 = GPIO.input(pin5)
    bits = [b3,b2,b1,b0]
    bits = [str(b) for b in bits]
    binary = "".join(bits)
    binary = int(binary,2)
    print(binary)
    time.sleep(0.2)
