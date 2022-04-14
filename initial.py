import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import subprocess
import time
import os
# Mount  RAMdrive
subprocess.run(["mount -a"],shell=True)
#Set drive and endpoint settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
direction_pin= 22 # Direction (DIR) GPIO Pin
step_pin = 23 # Step GPIO Pin
EN_pin = 24 # enable pin (LOW to enable)
steps_per_round =198 #(Default 198)
finish_point_pin=27
start_point_pin=17
GPIO.setup(start_point_pin,GPIO.IN)
GPIO.setup(finish_point_pin,GPIO.IN)
motor = RpiMotorLib.A4988Nema(direction_pin, step_pin, (21,21,21), "DRV8825")
GPIO.setup(EN_pin,GPIO.OUT) 
GPIO.output(EN_pin,GPIO.LOW) # pull enable to low to enable motor
# Function for return holder to start point (start_pin,number steps)

def go_home(start,steps):
#    GPIO.output(EN_pin,GPIO.LOW) # pull enable to low to enable motor
    while GPIO.input(start)==True:
        motor.motor_go(True, # True=Clockwise, False=Counter-Clockwise
                     "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                     steps, # number of steps
                     .001, # step delay [sec]
                     False, # True = print verbose output 
                     .05) # initial delay [sec]

    motor.motor_go(False, # True=Clockwise, False=Counter-Clockwise
                     "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                     steps, # number of steps
                     .001, # step delay [sec]
                     False, # True = print verbose output 
                     .05) # initial delay [sec]
    #GPIO.cleanup() # clear GPIO allocations after rungjhfrasp


go_home(start_point_pin,steps_per_round)
GPIO.cleanup() # clear GPIO allocations after rungjhfrasp