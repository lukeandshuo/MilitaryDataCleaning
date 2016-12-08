import os
from pandas import Series,DataFrame
import pandas  as pd
import time
#For Visible
AgtDir = "sample_data/AGT/Visible_agt/"
MetricDir = "sample_data/Metric/Visible/"
GTDir = "sample_data/GroundTruth/Visible_GT/"

#For IR
# AgtDir = "sample_data/AGT/IR_agt/"
# MetricDir = "sample_data/Metric/IR/"
# GTDir = "sample_data/GroundTruth/IR_GT/"

start = time.clock()
fileList = os.listdir(AgtDir)
for fName in fileList:
    if os.path.splitext(fName)[1] == ".csv":
        df_agt = pd.read_csv(AgtDir+fName)
        df_bbox = pd.read_csv(MetricDir+fName)
        BBoxW = 2*(df_agt["PixLocX"]-df_bbox["UpperLeft"])
        BBoxH = 2*(df_agt["PixLocY"]-df_bbox["UpperTop"])
        df_gt = DataFrame({"VideoName":df_agt["VideoName"],"Frame":df_agt["Frame"],"CenterX":df_agt["PixLocX"],"CenterY":df_agt["PixLocY"],
                           "UpperLeft":df_bbox["UpperLeft"],"UpperTop":df_bbox["UpperTop"],"BBoxW":BBoxW,"BBoxH":BBoxH,"Time":df_agt["Time"],
                           "TgtType":df_agt["TgtType"],"Distance":df_agt["Range"],"Area":df_bbox["Pot"],"Aspect":df_agt["Aspect"],"Speed":df_agt["Speed"],
                           "TgtSenRelAzimuth":df_agt["TgtSenRelAzimuth"],"TgtSenRelElevation":df_agt["TgtSenRelElevation"]}
                          ,columns=["VideoName","Frame","Time","CenterX","CenterY","UpperLeft","UpperTop","BBoxW","BBoxH","TgtType","Distance","Area","Aspect","Speed","TgtSenRelAzimuth","TgtSenRelElevation"])
        df_gt.to_csv(GTDir+fName,index=False)

end = time.clock()
print end-start