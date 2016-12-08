import cv2
import os
import pandas  as pd
import numpy as np
from pandas import Series,DataFrame
def DrawBox(BboxDir,ImageDir):
     BboxFile = os.listdir(BboxDir)[2]
     print BboxFile
     df_bbox = pd.read_csv(BboxDir+BboxFile)
     frame = df_bbox['Frame']
     videoName = df_bbox['VideoName']
     time = df_bbox['Time']
     x1 = df_bbox['UpperLeft']
     y1 = df_bbox['UpperTop']
     x2 = x1+df_bbox["BBoxW"]
     y2 = y1+df_bbox["BBoxH"]
     Type = df_bbox["TgtType"]
     Range = df_bbox["Distance"]
     Speed = df_bbox["Speed"]
     Aspect = df_bbox["Aspect"]

     for i in range(len(frame)):
          if x1[i]==-1 and y1[i]==-1:
               continue
          image_path = ImageDir + str(videoName[i])+"_"+str(frame[i])+".png"
          image = cv2.imread(image_path,1)
          image = ImproveBrightNess(image)
          cv2.rectangle(image,(x1[i]-5,y1[i]-5),(x2[i]+5,y2[i]+5),(0,255,0),2)
          cv2.putText(image, "Type:" + str(Type[i]), (x1[i], y1[i] - 100), 0, 0.6, (0, 0, 255))
          cv2.putText(image,"Range:"+str(Range[i]),(x1[i],y1[i]-70),0,0.6,(0,0,255))
          cv2.putText(image, "Speed:" + str(Speed[i]), (x1[i], y1[i] - 40), 0, 0.6, (0, 0, 255))
          cv2.putText(image, "Aspect:" + str(Aspect[i]), (x1[i], y1[i] - 10), 0, 0.6, (0, 0, 255))
          cv2.putText(image, "Frame:" + str(frame[i]), (0, 20), 0, 0.6, (255, 0, 255),2)
          cv2.putText(image, "Time:" + str(time[i]), (0, image.shape[0]-20), 0, 0.6, (255, 0, 255),2)
          cv2.imshow(BboxDir.split('/')[-1],image)
          cv2.waitKey(33)
          if i == 350:
               cv2.imwrite("Draw.png",image)
def ImproveBrightNess(image):
     if image.shape ==3:
          return cv2.equalizeHist(image)
     else:
          B,G,R = cv2.split(image)
          B = cv2.equalizeHist(B)
          G = cv2.equalizeHist(G)
          R = cv2.equalizeHist(R)
          return cv2.merge((B,G,R))

if __name__ == "__main__":
     #Drawing Visble
     V_BboxDir = "sample_data/GroundTruth/Visible_GT/"
     V_ImageDir = "sample_data/imagery/Visible_imagery/images/"
     DrawBox(V_BboxDir,V_ImageDir)
     #Drawing IR
     IR_BboxDir = "sample_data/GroundTruth/IR_GT/"
     IR_ImageDir = "sample_data/imagery/IR_imagery/images/"
     DrawBox(IR_BboxDir,IR_ImageDir)
