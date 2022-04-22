import subprocess
sample_name='test'
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
        print('Please reconnect camera and press Enter')
        input()