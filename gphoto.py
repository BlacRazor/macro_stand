import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import subprocess
import time
import os
#import shutil
from PIL import Image
# Mount  RAMdrive
subprocess.run(["mount -a"],shell=True)
#Set drive and endpoint settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
direction_pin= 22 # Direction (DIR) GPIO Pin
step_pin = 23 # Step GPIO Pin
EN_pin = 24 # enable pin (LOW to enable)
next_frame = 15
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
        motor.motor_go(False, # True=Clockwise, False=Counter-Clockwise
                     "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                    steps, # number of steps
                     .001, # step delay [sec]
                     False, # True = print verbose output 
                     .05) # initial delay [sec]

    motor.motor_go(True, # True=Clockwise, False=Counter-Clockwise
                     "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                    int(steps/2), # number of steps
                     .001, # step delay [sec]
                     False, # True = print verbose output 
                     .05) # initial delay [sec]
    #GPIO.cleanup() # clear GPIO allocations after rungjhfrasp

# Function for going to next point photo
def next_photo(finish,frame,steps):
#   GPIO.output(EN_pin,GPIO.LOW) # pull enable to low to enable motor
    iteration=0
    while iteration<frame:
        if GPIO.input(finish)==True:
            motor.motor_go(True, # True=Clockwise, False=Counter-Clockwise
                     "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                    steps, # number of steps
                     .001, # step delay [sec]
                     False, # True = print verbose output 
                     .05) # initial delay [sec]
        else:
            print('End linear guide')
            iteration=frame
            motor.motor_go(False, # True=Clockwise, False=Counter-Clockwise
                     "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                    int(steps/2), # number of steps
                     .001, # step delay [sec]
                     False, # True = print verbose output 
                     .05) # initial delay [sec]

        iteration+=1
    #GPIO.cleanup() 

finish_work=False
while finish_work!=True:
  # Get Sample name and create folder for photo
  print("Please input sample name and press Enter:")
  sample_name = input()
  subprocess.run(["mkdir /home/pi/project/RAMdrive/"+sample_name],shell=True)
  os.chdir("/home/pi/project/RAMdrive/"+sample_name)
  # Get sample lenght and decide count photo
  print("Please input sample lenght(cm) and press Enter:")
  sample_lenght = int(input())
  sample_count = int(sample_lenght/3)+1
  print("Count photo: "+str(sample_count))
  photo_range=[]
  # Take Photo from DSLR
  for i in range(sample_count):
    result=subprocess.run(["gphoto2 --capture-image-and-download --filename "+sample_name+"_"+str(i)+".jpg"],shell=True)
    photo_range.append(sample_name+"_"+str(i)+".jpg")
    next_photo(finish_point_pin,next_frame,steps_per_round)

  print(photo_range)
  go_home(start_point_pin,steps_per_round)
  images = [Image.open(x) for x in photo_range]
  widths, heights = zip(*(i.size for i in images))

  total_width = sum(widths)-(len(widths)*100)
  max_height = max(heights)

  new_im = Image.new('RGB', (total_width, max_height))

  x_offset = 0
  for im in images:
    new_im.paste(im, (x_offset,0))
    x_offset += im.size[0]-100

  # Склейка в стык
  #x_offset = 0
  #for im in images:
  #  new_im.paste(im, (x_offset,0))
  #  x_offset += im.size[0]

  new_im.save(sample_name+'.jpg')

  # Open folder with photo
  subprocess.run(["pcmanfm"],shell=True)
  #shutil.copytree("/home/pi/project/RAMdrive/"+sample_name,"/home/pi/project/smb/"+sample_name)
  subprocess.run(["cp -r /home/pi/project/RAMdrive/"+sample_name+" /home/pi/Pictures/sampls/"+sample_name],shell=True)
  subprocess.run(["cp -r /home/pi/project/RAMdrive/"+sample_name+" /home/pi/project/smb/"+sample_name],shell=True)

  

  print('Retry with new sample (Yy/Nn)?')     
  if input().lower()=="n":        
    finish_work=True
GPIO.cleanup() # clear GPIO allocations after rungjhfrasp