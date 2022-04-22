import subprocess
sample_name='test'
i=1
result=subprocess.run(["gphoto2 --capture-image-and-download --filename "+sample_name+"_"+str(i)+".jpg"],shell=True)
print(result)
