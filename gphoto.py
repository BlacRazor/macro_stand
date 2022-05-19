import RPi.GPIO as GPIO
import math
from RpiMotorLib import RpiMotorLib
import subprocess
import time
import os
#import shutil
from PIL import Image
subprocess.run(["/bin/python /home/pi/macro_stand/initial.py"],shell=True)

#Set drive and endpoint settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# 34mm minimal frame size
# 7mm travel per round
# 19steps on one mm travel
step_per_mm=25
# Half linear beams for compute start position
half_line=400

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
                     "1/4" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                    steps_to_home, # number of steps
                     .001, # step delay [sec]
                     False, # True = print verbose output 
                     .005) # initial delay [sec]
    small_steps=int(198/4)
    while GPIO.input(start)==True:
        motor.motor_go(True, # True=Clockwise, False=Counter-Clockwise
                     "1/8" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
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
                     "1/8" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                    steps, # number of steps
                     .00095, # step delay [sec]
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
def go_start_position(steps,direction):
  motor.motor_go(direction, # True=Right->Left, False=Left->Right
                     "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                    steps, # number of steps
                     .001, # step delay [sec]
                     False, # True = print verbose output 
                     .05) # initial delay [sec]
finish_work=False
while finish_work!=True:
  print('1. Install sample on holder and press Enter to continue')
  input()
  go_start_position(half_line*step_per_mm,False)
  # Get frame size
  print("2. Check conection and AF camera! (fix connection - on/off camera). Off AF on lens!")
  print("Input frame size in mm (minimal 34mm):")
  frame_size=int(input())
  # Get sample lenght and decide count photo
  print("3. Input sample length(mm) and press Enter:")
  sample_lenght = int(input())
  # Get Sample name and create folder for photo
  print("4. Input sample name and press Enter (without spaces):")
  sample_name = input()
  subprocess.run(["mkdir /home/pi/project/RAMdrive/"+sample_name],shell=True)
  os.chdir("/home/pi/project/RAMdrive/"+sample_name)
  crossing=0
  print("5. Input number choise frame crossing (only variant 1,2 or 3):")
  print("1) 1/4")
  print("2) 1/2")
  print("3) 3/4")
  crossing=int(input())
  if crossing==1:
    frame_size=frame_size-(frame_size*0.25)
    steps_per_frame=math.ceil(frame_size*step_per_mm)
    sample_count=math.ceil(sample_lenght/frame_size)
    sleep=1
  elif crossing==2:
    frame_size=frame_size-int(frame_size*0.5)
    steps_per_frame=math.ceil(frame_size*step_per_mm)
    sample_count=math.ceil(sample_lenght/frame_size)
    sleep=2
  else:
    frame_size=frame_size-int(frame_size*0.75)
    steps_per_frame=math.ceil(frame_size*step_per_mm)
    sample_count=math.ceil(sample_lenght/frame_size)
    sleep=3

  size_full_frame=sample_count*frame_size
  ofset=size_full_frame-sample_lenght
  if ofset<(frame_size/4):
      sample_count=sample_count+1
  size_full_frame=sample_count*frame_size
  ofset=size_full_frame-sample_lenght
  
  steps_to_start=math.ceil((sample_lenght/2)*step_per_mm)

  #sample_count = int(sample_lenght/frame_size)+1
  print("Count photo: "+str(sample_count))
  photo_range=[]
  go_start_position(steps_to_start,True)
  # Take Photo from DSLR
  for i in range(sample_count):
    ok=False
    atempt=0
    while ok==False:
      result=subprocess.run(["gphoto2 --capture-image-and-download --filename "+sample_name+"_"+str(i)+".jpg"],shell=True,capture_output=True, text=True)
      if result.stderr!='':
        ok=False
        print('Warning: fail camera: '+result.stderr)
        atempt=atempt+1
      else:
        ok=True
        atempt=0
      if atempt>10:
        print('Please reboote stand and restart process')
        exit()
      if atempt>5:
        print('Please reconnect camera (When you touch shot button on camera on visor show "Bussy" or display show PC icon!) and press Enter')
        input()
    photo_range.append(sample_name+"_"+str(i)+".jpg")
    next_photo(finish_point_pin,steps_per_frame)
    #time.sleep(sleep)

  num_steps_to_home=int((steps_per_frame)*(sample_count-1)+steps_to_start*2-100)
  print(photo_range)
  go_home(start_point_pin,num_steps_to_home)
  images = [Image.open(x) for x in photo_range]
  widths, heights = zip(*(i.size for i in images))
  
  if crossing==1:
    cros_pixel=widths[0]-math.ceil(widths[0]*0.75)
  elif crossing==2:
    cros_pixel=widths[0]-math.ceil(widths[0]*0.5)
  else: 
    cros_pixel=widths[0]-math.ceil(widths[0]*0.25)
    
  total_width = sum(widths)-(len(widths)*cros_pixel)
  max_height = max(heights)
  new_im = Image.new('RGB', (total_width, max_height))
  x_offset = 0
  for im in images:
    new_im.paste(im, (x_offset,0))
    x_offset += im.size[0]-cros_pixel-75
  
  new_im.save(sample_name+'_h.jpg')
  new_im_v=new_im.rotate(-90, Image.NEAREST, expand = 1)
  new_im_v.save(sample_name+'_v.jpg')

  # Open folder with photo
  subprocess.run(["pcmanfm"],shell=True)
  #shutil.copytree("/home/pi/project/RAMdrive/"+sample_name,"/home/pi/project/smb/"+sample_name)
  subprocess.run(["sudo cp -r /home/pi/project/RAMdrive/"+sample_name+" /home/pi/Pictures/samples/"+sample_name],shell=True)
  subprocess.run(["sudo cp -r /home/pi/project/RAMdrive/"+sample_name+" /home/pi/project/smb/"+sample_name],shell=True)

  

  print('Retry with new sample (Yy/Nn)?')     
  if input().lower()=="n":        
    finish_work=True
GPIO.cleanup() # clear GPIO allocations after rungjhfrasp
