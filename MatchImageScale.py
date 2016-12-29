import cv2
import os
import pandas  as pd
import numpy as np
from pandas import Series,DataFrame
def DrawBoxIR(BboxDir,ImageDir):
     BboxFile = os.listdir(BboxDir)[2]
     print BboxFile
     df_bbox = pd.read_csv(BboxDir+BboxFile)
     frame = df_bbox['Frame']
     videoName = df_bbox['VideoName']


     for i in range(len(frame)):
          image_path = ImageDir + str(videoName[i])+"_"+str(frame[i])+".png"
          image = cv2.imread(image_path,0)
          image = ImproveBrightNess(image)
          cv2.imshow(BboxDir.split('/')[-1],image)
          cv2.waitKey(33)


def DrawBoxV(BboxDir, ImageDir):
    BboxFile = os.listdir(BboxDir)[2]
    print BboxFile
    df_bbox = pd.read_csv(BboxDir + BboxFile)
    frame = df_bbox['Frame']
    videoName = df_bbox['VideoName']

    for i in range(len(frame)):
        image_path = ImageDir + str(videoName[i]) + "_" + str(frame[i]) + ".png"
        image = cv2.imread(image_path, 0)
        image = ImproveBrightNess(image)
        if i ==2:
            cv2.imwrite("sample.png",image)
        cv2.imshow(BboxDir.split('/')[-1], image)
        cv2.waitKey(33)

def ImproveBrightNess(image):
     if len(image.shape) ==2: #single channel
          return cv2.equalizeHist(image)
     else:
          B,G,R = cv2.split(image)
          B = cv2.equalizeHist(B)
          G = cv2.equalizeHist(G)
          R = cv2.equalizeHist(R)
          return cv2.merge((B,G,R))

if __name__ == "__main__":
     #Drawing Visble
     V_BboxDir = "sample_data/GroundTruth/Visible/"
     V_ImageDir = "sample_data/imagery/Visible/images/"
     DrawBoxV(V_BboxDir,V_ImageDir)
     #Drawing IR
     IR_BboxDir = "sample_data/GroundTruth/IR/"
     IR_ImageDir = "sample_data/imagery/IR/images/"
     DrawBoxIR(IR_BboxDir,IR_ImageDir)