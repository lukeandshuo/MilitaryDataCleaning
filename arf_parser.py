import xdrlib
from struct import *
import os
import cv2
import numpy as np
import time
Dir = "sample_data/Imagery/Visible_imagery/"
VideoDir = Dir+"videos/"
fileList = os.listdir(VideoDir)
start = time.clock()
print fileList
for f in fileList:
    if os.path.splitext(f)[1] =='.arf':
        with open(VideoDir+f,"rb") as file:
            print f
            magic_num = unpack(">I",file.read(4))[0]
            version = unpack(">I",file.read(4))[0]
            rows = unpack(">I",file.read(4))[0]
            cols = unpack(">I",file.read(4))[0]
            image_type = unpack(">I",file.read(4))[0]
            num_frames = unpack(">I",file.read(4))[0]
            image_offset = unpack(">I",file.read(4))[0]
            file.seek(image_offset)
            print rows,cols,image_offset,image_type,num_frames
            for i in range(num_frames):
                print i
                frame = np.zeros((rows,cols,1),np.ushort)

                for r in range(rows):
                    for c in range(cols):
                        frame[r,c] = unpack(">H",file.read(2))[0]
                name = Dir+"images/"+os.path.splitext(f)[0]+"_"+str(i+1)+".png"
                cv2.imwrite(name,frame)
                # im = cv2.imread(name,cv2.IMREAD_GRAYSCALE)
                # imc=cv2.applyColorMap(im,cv2.COLORMAP_HSV)
                # cv2.imwrite(name,imc)
end = time.clock()
print end-start
