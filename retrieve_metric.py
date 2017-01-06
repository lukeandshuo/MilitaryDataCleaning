
from __future__ import division
import pandas
from pandas import DataFrame, Series
import os
import cv2
import numpy as np
IR_H = 512
IR_W = 640
V_H = 480
V_W = 640
MetricDir = "sample_data/Metric/"
IRMetricDir = MetricDir + "IR/"
VisibleMetricDir = MetricDir + "Visible/"

IRImgDir = "sample_data/Imagery/IR/images/"
IRImgRegDir="sample_data/Imagery/IR_Reg/images/"


AGTDir = "sample_data/AGT/"
IRAGTDir = AGTDir+"IR/"
VisAGTDir = AGTDir + "Visible/"
VisImgDir = "sample_data/Imagery/Visible/images/"

def GetTime(Time):
    Time = Time.split('/')
    return int(Time[-1])+int(Time[-2])*1000+int(Time[-3])*60
def GetMatchIndex(series,target):
    index = 0
    distance = 100000
    for i,time in enumerate(series):
        if abs(target-GetTime(time))<distance:
            distance=abs(target-GetTime(time))
            index = i
    return index
def SearchName(name,name_list):
    for n in name_list:
        if name[4:] == n[4:]:
            print n
            return n
    print "no found"
    return "not found"
def RegisterImg(IRname,IRFovW,IRFovH,IRCX,IRCY,Visname,VisFovW,VisFovH,VisCX,VisCY):
    IRImgPath = IRImgDir + IRname
    VisImgPath = VisImgDir + Visname
    IRImg = cv2.imread(IRImgPath)
    VisImg = cv2.imread(VisImgPath)
    RatFW = IRFovW / VisFovW
    print "RatFW",RatFW
    RatFH = IRFovH / VisFovH
    print "RatFH",RatFH
    Scale = np.maximum(RatFW,RatFH)
    print "Scale",Scale

    IRImg = cv2.resize(IRImg, None, None, fx=Scale, fy=Scale, interpolation=cv2.INTER_LINEAR)
    ShiftX = VisCX-IRCX*Scale
    ShiftY = VisCY-IRCY*Scale
    M = np.float32([[1,0,ShiftX],[0,1,ShiftY]])
    rows = VisImg.shape[0]
    cols = VisImg.shape[1]
    IRImg = cv2.warpAffine(IRImg, M, (cols, rows))
    if not os.path.exists(IRImgRegDir):
        print "no path"
        os.makedirs(IRImgRegDir)
    IRImgRegPath = IRImgRegDir + IRname
    print IRImgRegPath
    cv2.imwrite(IRImgRegPath,IRImg)

    VTest = False
    if VTest:
        cv2.circle(IRImg,(VisCX,VisCY),5,(0,0,255))
        cv2.circle(VisImg,(VisCX,VisCY),5,(0,255,0))
        Img = np.concatenate((IRImg,VisImg),axis=1)
        cv2.imshow("result",Img)
        cv2.waitKey(1)


IRMfile = os.listdir(IRMetricDir)
VMfile = os.listdir(VisibleMetricDir)

IRagtFile = os.listdir(IRAGTDir)
VagtFile =  os.listdir(VisAGTDir)
print IRagtFile
print VagtFile
for i,f in enumerate(IRMfile):
    if os.path.splitext(f)[1] == ".csv" and int(os.path.splitext(f)[0][5:9])>2000:
        print "num:"+ str(os.path.splitext(f)[0][5:9])
        print "file name:",f
        df_IRM = pandas.read_csv(IRMetricDir+f)
        df_IRagt = pandas.read_csv(IRAGTDir+f)
        ExistFile = SearchName(f,VMfile)
        if ExistFile != "not found":
            print f,"has been processed"
            continue
        Vname = SearchName(f, VagtFile)
        assert Vname != "not found"
        df_Vagt = pandas.read_csv(VisAGTDir+ Vname)
        if df_Vagt['TgtType'][0]== "MAN": # do not process pedestrain
            print df_Vagt['Time'][0]
            continue
        IR = DataFrame({'VideoName':df_IRagt['VideoName'],'Frame':df_IRagt["Frame"],"Time":df_IRagt['Time'],"FW":df_IRagt['FovW'],"FH":df_IRagt['FovH'],"CX":df_IRagt['PixLocX'],"CY":df_IRagt['PixLocY'],"X1":df_IRM['UpperLeft'],"Y1":df_IRM['UpperTop']})
        Visible = DataFrame({'VideoName':df_Vagt['VideoName'],'Frame':df_Vagt['Frame'],'Time':df_Vagt['Time'],'FW':df_Vagt['FovW'],'FH':df_Vagt['FovH'],'CX':df_Vagt['PixLocX'],'CY':df_Vagt['PixLocY']})
        Vsize = len(Visible['Time'])
        IRsize = len(IR['Time'])
        print Vsize,IRsize

        print Visible['Time'][Vsize-1]
        print IR['Time'][IRsize-1]
        if len(str(Visible['Time'][Vsize-1]))< 4:
            print "Two target in",f
            continue
        if len(str(IR['Time'][IRsize-1]))<4:
            print "Two target in",f
            continue
        IR_start = 0
        V_start = 0
        IR_t = GetTime(IR['Time'][0])
        V_t = GetTime(Visible['Time'][0])
        if IR_t > V_t:
            V_start = GetMatchIndex(Visible['Time'],IR_t)
        else:
            IR_start = GetMatchIndex(IR['Time'],V_t)

        print "IR start point",IR_start,"visible start point ",V_start
        print IR['Time'][IR_start],Visible['Time'][V_start]

        V_X1 = []
        V_Y1 = []
        Match = []
        increment = 0
        count =0
        for i in range(len(Visible['Frame'])):
            if i < V_start:
                V_X1.append(-1)
                V_Y1.append(-1)
                Match.append(" ")
            else:
                j = IR_start+increment
                if j < len(IR['Frame']): # find match image
                    X1 = Visible['CX'][i]-(float(IR['CX'][j]-IR['X1'][j])/float(IR_W))*V_W
                    V_X1.append(int(X1))
                    Y1 = Visible['CY'][i]-(float(IR['CY'][j]-IR['Y1'][j])/float(IR_H))*V_H
                    V_Y1.append(int(Y1))

                    # print IR['VideoName'][j]
                    # print IR['Frame'][j]
                    MatchName = str(IR['VideoName'][j])+"_"+str(IR['Frame'][j])
                    # print MatchName
                    Match.append(MatchName)
                    IRImgName= str(IR['VideoName'][j])+'_'+str(IR['Frame'][j])+'.png'
                    VisImgName = str(Visible['VideoName'][i]) + '_' + str(Visible['Frame'][i])+ '.png'
                    print IRImgName,VisImgName
                    #register both images
                    RegisterImg(IRImgName,IR['FW'][j],IR['FH'][j],IR['CX'][j],IR['CY'][j],VisImgName,Visible['FW'][i],Visible['FH'][i],Visible['CX'][i],Visible['CY'][i])
                    count +=1
                else:
                    V_X1.append(-1)
                    V_Y1.append(-1)
                    Match.append(" ")
                increment += 1
        print "count:",count
        X1=Series(V_X1)
        Y1=Series(V_Y1)
        Match = Series(Match)
        W = (Visible['CX']-X1)*2
        H = (Visible['CY']-Y1)*2
        Pot = H*W
        VisibleMetric = DataFrame({"VideoName":df_Vagt['VideoName'],"Frame":df_Vagt['Frame'],"Pot":Pot,"UpperLeft":X1,"UpperTop":Y1,"Match":Match})

        Name = VisibleMetricDir+df_Vagt['VideoName'][0]+".csv"
        VisibleMetric.to_csv(Name,index=False)
