import os
import os.path as op
from pandas import Series,DataFrame
import pandas  as pd
import time
ImgType = "IR"

AgtDir = op.join("sample_data/AGT",ImgType)
MetricDir = op.join("sample_data/Metric",ImgType)
GTDir = op.join("sample_data/GroundTruth",ImgType)

start = time.clock()
fileList = os.listdir(AgtDir)
for fName in fileList:
    if os.path.splitext(fName)[1] == ".csv":
        df_agt = pd.read_csv(op.join(AgtDir,fName))
        df_bbox = pd.read_csv(op.join(MetricDir,fName))
        BBoxW = 2*(df_agt["PixLocX"]-df_bbox["UpperLeft"])
        BBoxH = 2*(df_agt["PixLocY"]-df_bbox["UpperTop"])
        ImageName = df_agt["VideoName"].astype(str)+"_"+df_agt["Frame"].astype(str)
        df_gt = DataFrame({"VideoName":df_agt["VideoName"],"Frame":df_agt["Frame"],"ImageName":ImageName,"CenterX":df_agt["PixLocX"],"CenterY":df_agt["PixLocY"],
                           "UpperLeft":df_bbox["UpperLeft"],"UpperTop":df_bbox["UpperTop"],"BBoxW":BBoxW,"BBoxH":BBoxH,"Time":df_agt["Time"],
                           "TgtType":df_agt["TgtType"],"Distance":df_agt["Range"],"Area":df_bbox["Pot"],"Aspect":df_agt["Aspect"],"Speed":df_agt["Speed"],
                           "TgtSenRelAzimuth":df_agt["TgtSenRelAzimuth"],"TgtSenRelElevation":df_agt["TgtSenRelElevation"]}
                          ,columns=["VideoName","Frame","ImageName","Time","CenterX","CenterY","UpperLeft","UpperTop","BBoxW","BBoxH","TgtType","Distance","Area","Aspect","Speed","TgtSenRelAzimuth","TgtSenRelElevation"])
        if df_agt["VideoName"][1][:4] == "i1co":
            df_gt["Match"] = df_bbox["Match"]
        df_gt.to_csv(op.join(GTDir,fName),index=False)

end = time.clock()
print end-start