import cv2
import os
import pandas  as pd
import numpy as np
from pandas import Series,DataFrame
def DrawBox(V_FGT,IR_FGT,VImageDir,IRImageDir):
     v_bbox = pd.read_csv(V_FGT)
     ImageName = v_bbox['ImageName']
     Type = v_bbox['TgtType']
     Range = v_bbox['Distance']
     MatchName = v_bbox['Match']
     ir_bbox = pd.read_csv(IR_FGT)
     for i in range(0,len(ImageName),10):
          if MatchName[i].strip() == "":
               continue
          #select
          # if Type[i] != "ZSU23":
          #      continue
          if float(Range[i]) < 0:
               continue
          print MatchName[i]
          # for IR image
          IRimage_path = IRImageDir + MatchName[i]+".png"
          IRimage = cv2.imread(IRimage_path)
          ir_i = ir_bbox[ir_bbox['ImageName']==MatchName[i]].index.tolist()
          IRimage=DrawInfo(IRimage,ir_bbox,ir_i[0])
          # cv2.imshow("IR", IRimage)
          #for visible Image
          Vimage_path = VImageDir+ImageName[i]+".png"
          Vimage = cv2.imread(Vimage_path)
          Vimage = DrawInfo(Vimage,v_bbox,i)
          # cv2.imshow("V",Vimage)
          vis = np.concatenate((IRimage,Vimage),axis=0)
          cv2.imshow("final",vis)
          cv2.waitKey(1)

def DrawInfo(image,df_bbox,i):
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
     image = ImproveBrightNess(image)
     cv2.rectangle(image, (x1[i] - 5, y1[i] - 5), (x2[i] + 5, y2[i] + 5), (0, 255, 0), 2)
     cv2.putText(image, "Type:" + str(Type[i]), (x1[i], y1[i] - 100), 0, 0.6, (0, 0, 255))
     cv2.putText(image, "Range:" + str(Range[i]), (x1[i], y1[i] - 70), 0, 0.6, (0, 0, 255))
     cv2.putText(image, "Speed:" + str(Speed[i]), (x1[i], y1[i] - 40), 0, 0.6, (0, 0, 255))
     cv2.putText(image, "Aspect:" + str(Aspect[i]), (x1[i], y1[i] - 10), 0, 0.6, (0, 0, 255))
     cv2.putText(image, "Frame:" + str(frame[i]), (0, 20), 0, 0.6, (255, 0, 255), 2)
     cv2.putText(image, str(videoName[i]), (image.shape[1]/3, 20), 0, 0.6, (255, 0, 255), 2)
     cv2.putText(image, "Time:" + str(time[i]), (0, image.shape[0] - 20), 0, 0.6, (255, 0, 255), 2)
     return image

def ImproveBrightNess(image):
     if image.shape == 3:
          return cv2.equalizeHist(image)
     else:
          B,G,R = cv2.split(image)
          B = cv2.equalizeHist(B)
          G = cv2.equalizeHist(G)
          R = cv2.equalizeHist(R)
          return cv2.merge((B,G,R))

if __name__ == "__main__":
     #Drawing Visble
     V_FGT = "sample_data/GroundTruth/Visible_GT/FullList.csv"
     IR_FGT = "sample_data/GroundTruth/IR_GT/FullList.csv"
     V_ImageDir = "sample_data/Imagery/Visible_imagery/images/"
     IR_ImageDir = "sample_data/Imagery/IR_imagery/images/"
     DrawBox(V_FGT,IR_FGT,V_ImageDir,IR_ImageDir)
     #Drawing IR
     # IR_BboxDir = "sample_data/GroundTruth/IR_GT/"
     # IR_ImageDir = "sample_data/imagery/IR_imagery/images/"
     # DrawBox(IR_BboxDir,IR_ImageDir)
