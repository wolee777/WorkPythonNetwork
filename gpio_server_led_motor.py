import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( False )

led1 = 14
led2 = 15

MOTOR_P = 4
MOTOR_N = 25
MOTOR_EN = 12

def led_init():
    GPIO.setup( led1, GPIO.OUT )
    GPIO.setup( led2, GPIO.OUT )

def led_1_on():
    GPIO.output( led1, True )

def led_2_on():
    GPIO.output( led2, True )

def led_1_off():
    GPIO.output( led1, False )

def led_2_off():
    GPIO.output( led2, False )

def led_all_on():
    led_1_on()
    led_2_on()

def led_all_off():
    led_1_off()
    led_2_off()

def led_blink():
    for _ in range( 1, 6 ):
        led_1_on()
        led_2_on()
        time.sleep( 0.3 )
        led_1_off()
        led_2_off()
        time.sleep( 0.3 )

def motor_init():
    GPIO.setup( MOTOR_P, GPIO.OUT )
    GPIO.setup( MOTOR_N, GPIO.OUT )
    GPIO.setup( MOTOR_EN, GPIO.OUT )

def motor_forword():
    print( 'forword' )
    GPIO.output( MOTOR_P, True )
    GPIO.output( MOTOR_N, False )
    GPIO.output( MOTOR_EN, True )
    time.sleep( 1 )

def motor_backword():
    print( 'backword' )
    GPIO.output( MOTOR_P, False )
    GPIO.output( MOTOR_N, True )
    GPIO.output( MOTOR_EN, True )
    time.sleep( 1 )

def motor_stop():
    GPIO.output( MOTOR_EN, False )

def gpio_cleanup():
    GPIO.cleanup()
