from PIL import Image
import math
photo_range=[]
sample_count=15
sample_name='22.04.1_2'
crossing=2
for i in range(sample_count):
    photo_range.append(sample_name+"_"+str(i)+".jpg")

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