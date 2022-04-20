import math
step_per_mm=19
print('frame')
frame_size=int(input())
print('size')
sample_lenght=int(input())

print("Input number choise frame crossing (only variant 1,2 or 3):")
print("1) 1/4")
print("2) 1/2")
print("3) 3/4")
crossing=int(input())
if crossing==1:
  frame_size=frame_size-(frame_size*0.25)
  steps_per_frame=math.ceil(frame_size*step_per_mm)
  count_frame=math.ceil(sample_lenght/frame_size)
elif crossing==2:
  frame_size=frame_size-int(frame_size*0.5)
  steps_per_frame=math.ceil(frame_size*step_per_mm)
  count_frame=math.ceil(sample_lenght/frame_size)
else:
  frame_size=frame_size-int(frame_size*0.75)
  steps_per_frame=math.ceil(frame_size*step_per_mm)
  count_frame=math.ceil(sample_lenght/frame_size)
  
size_full_frame=count_frame*frame_size
ofset=size_full_frame-sample_lenght
if ofset<(frame_size/2):
    count_frame=count_frame+1
size_full_frame=count_frame*frame_size
ofset=size_full_frame-sample_lenght
steps_to_start=math.ceil((480-(sample_lenght+ofset/2))*step_per_mm)

print(sample_lenght)
print(count_frame)
print(size_full_frame)
print(steps_per_frame)
print(ofset)

