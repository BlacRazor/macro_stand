import subprocess
sample_name='test'
i=1
result=subprocess.run(["gphoto2 --capture-image-and-download --filename "+sample_name+"_"+str(i)+".jpg"],shell=True,capture_output=True, text=True)
print("stdout:", result.stdout)
print("stderr:", result.stderr)
