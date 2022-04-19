import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import subprocess
import time
import os
#import shutil
from PIL import Image
#Set drive and endpoint settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# 34mm minimal frame size
# 7mm travel per round
# 19steps on one mm travel
step_per_mm=19
direction_pin= 22 # Direction (DIR) GPIO Pin
step_pin = 23 # Step GPIO Pin
EN_pin = 24 # enable pin (LOW to enable)
next_frame = 4 # cout round to next frame
view_frame=3 # Count on devision lenghtsample
steps_per_round =198 #(Default 198)
finish_point_pin=27
start_point_pin=17
GPIO.setup(start_point_pin,GPIO.IN)
GPIO.setup(finish_point_pin,GPIO.IN)

motor = RpiMotorLib.A4988Nema(direction_pin, step_pin, (21,21,21), "DRV8825")
GPIO.setup(EN_pin,GPIO.OUT) 
GPIO.output(EN_pin,GPIO.LOW) # pull enable to low to enable motor
# Function for return holder to start point (start_pin,number steps)
def go_home(start,steps_to_home):
#    GPIO.output(EN_pin,GPIO.LOW) # pull enable to low to enable motor
    
    motor.motor_go(True, # True=Clockwise, False=Counter-Clockwise
                     "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                    steps_to_home, # number of steps
                     .001, # step delay [sec]
                     False, # True = print verbose output 
                     .05) # initial delay [sec]
    small_steps=int(198/4)
    while GPIO.input(start)==True:
        motor.motor_go(True, # True=Clockwise, False=Counter-Clockwise
                     "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                    small_steps, # number of steps
                     .001, # step delay [sec]
                     False, # True = print verbose output 
                     .05) # initial delay [sec]

    motor.motor_go(False, # True=Clockwise, False=Counter-Clockwise
                     "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                    int(198/2), # number of steps
                     .001, # step delay [sec]
                     False, # True = print verbose output 
                     .05) # initial delay [sec]
    #GPIO.cleanup() # clear GPIO allocations after rungjhfrasp

# Function for going to next point photo
def next_photo(finish,steps):
#   GPIO.output(EN_pin,GPIO.LOW) # pull enable to low to enable motor
  if GPIO.input(finish)==True:
    motor.motor_go(False, # True=Clockwise, False=Counter-Clockwise
                     "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                    steps, # number of steps
                     .001, # step delay [sec]
                     False, # True = print verbose output 
                     .05) # initial delay [sec]
  else:
    motor.motor_go(True, # True=Clockwise, False=Counter-Clockwise
                     "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                    int(steps/2), # number of steps
                     .001, # step delay [sec]
                     False, # True = print verbose output 
                     .05) # initial delay [sec]
    #GPIO.cleanup() 
def go_start_position(steps):
  motor.motor_go(False, # True=Clockwise, False=Counter-Clockwise
                     "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                    steps, # number of steps
                     .001, # step delay [sec]
                     False, # True = print verbose output 
                     .05) # initial delay [sec]
finish_work=False
print("Input frame size in mm (minimal 34mm:")
frame_size=int(input())
while finish_work!=True:
  # Get Sample name and create folder for photo
  print("Input sample name and press Enter:")
  sample_name = input()
  subprocess.run(["mkdir /home/pi/project/RAMdrive/"+sample_name],shell=True)
  os.chdir("/home/pi/project/RAMdrive/"+sample_name)
  # Get sample lenght and decide count photo
  print("Input sample lenght(mm) and press Enter:")
  sample_lenght = int(input())
  sample_lenght = sample_lenght+int(frame_size*0.5)
  steps_to_start=int((405-int(sample_lenght/2)+int(frame_size*0.5))*step_per_mm)
  crossing=0
  print("Input number choise frame crossing (only variant 1,2 or 3):")
  print("1) 1/4")
  print("2) 1/2")
  print("3) 3/4")
  crossing=int(input())
  #sample_count = int(sample_lenght/frame_size)
  if crossing==1:
    #sample_count=int(sample_count*1,25)
    frame_size=frame_size-int(frame_size*0.25)
    steps_per_frame=int(frame_size*step_per_mm)
    sample_count=int(sample_lenght/frame_size)
  elif crossing==2:
    frame_size=frame_size-int(frame_size*0.5)
    steps_per_frame=int(frame_size*step_per_mm)
    sample_count=int(sample_lenght/frame_size)    
    #sample_count=int(sample_count*1,75)
  else:
    frame_size=frame_size-int(frame_size*0.75)
    steps_per_frame=int(frame_size*step_per_mm)
    sample_count=int(sample_lenght/frame_size)    
    #sample_count=int(sample_count*3,25)

  #sample_count = int(sample_lenght/frame_size)+1
  print("Count photo: "+str(sample_count))
  photo_range=[]
  go_start_position(steps_to_start)
  # Take Photo from DSLR
  for i in range(sample_count):
    result=subprocess.run(["gphoto2 --capture-image-and-download --filename "+sample_name+"_"+str(i)+".jpg"],shell=True)
    photo_range.append(sample_name+"_"+str(i)+".jpg")
    next_photo(finish_point_pin,steps_per_frame)
    time.sleep(3)

  num_steps_to_home=(steps_per_frame)*(sample_count-1)
  print(photo_range)
  go_home(start_point_pin,num_steps_to_home)
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
  subprocess.run(["sudo cp -r /home/pi/project/RAMdrive/"+sample_name+" /home/pi/Pictures/samples/"+sample_name],shell=True)
  subprocess.run(["sudo cp -r /home/pi/project/RAMdrive/"+sample_name+" /home/pi/project/smb/"+sample_name],shell=True)

  

  print('Retry with new sample (Yy/Nn)?')     
  if input().lower()=="n":        
    finish_work=True
GPIO.cleanup() # clear GPIO allocations after rungjhfrasp