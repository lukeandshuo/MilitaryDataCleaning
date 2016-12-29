from pandas import Series,DataFrame
import pandas as pd
import numpy as np
import os
def paserFile(path):
    fileOnlyName = ("/").join(path.split('.')[:-1]) #remove extension
    print fileOnlyName
    with open(path,'r') as file:
        start = False
        VideoName = []
        Time = []
        Speed = []
        VelStdDev = []
        VelEast =[]
        VelNorth = []
        VelUp = []
        SlantRange =[]
        Heading =[]
        TgtSenRelAzimuth =[]
        TgtSenRelElevation =[]
        PlyId =[]
        Range = []
        PixLocX =[]
        PixLocY =[]
        Aspect =[]
        TgtType =[]
        for line in file:
            line = line.strip('\n')
            line = line.strip() #remove space
            # print line

            if line == "TgtSect":
                start = True
            words = line.split()
            if start:
                for i,w in enumerate(words):
                    w = w.strip("\"")
                    if w == "Time":
                        words[i + 6]=words[i+6].zfill(3)
                        words[i + 5]=words[i+5].zfill(2)
                        words[i + 4]=words[i+4].zfill(2)
                        Time.append("/".join(words[i+1:i+7]))
                    if w == "Speed":
                        Speed.append(words[i+1])
                    if w == "VelStdDev":
                        VelStdDev.append(words[i+1])
                    if w == "VelEast":
                        VelEast.append(words[i+1])
                    if w == "VelNorth":
                        VelNorth.append(words[i+1])
                    if w == "VelUp":
                        VelUp.append(words[i+1])
                    if w == "SlantRange":
                        SlantRange.append(words[i+1])
                    if w == "Heading":
                        Heading.append(words[i+1].strip("\""))
                    if w == "TgtSenRelAzimuth":
                        TgtSenRelAzimuth.append(words[i+1].strip("\""))
                    if w == "TgtSenRelElevation":
                        TgtSenRelElevation.append(words[i+1].strip("\""))
                    if w == "Range":
                        Range.append(words[i+1])
                    if w == "PlyId":
                        PlyId.append(words[i+1].strip("\""))
                    if w == "PixLoc":
                        PixLocX.append(words[i+1])
                        PixLocY.append(words[i+2])
                    if w == "Aspect":
                        Aspect.append(words[i+1])
                    if w == "TgtType":
                        TgtType.append(words[i+1].strip("\""))
            else:
                for i,w in enumerate(words):
                    w = w.strip("\"")
                    if w == "Name":
                        VideoName.append(words[i+1].strip("\""))

        print "Time:",len(Time)
        # print "Speed",len(Speed)
        # print "SpeVelStdDeved",len(VelStdDev)
        # print "VelEast",len(VelEast)
        # print "VelNorth",len(VelNorth)
        # print "VelUp",len(VelUp)
        # print "SlantRange",len(SlantRange)
        # print "Heading",len(Heading)
        # print "TgtSenRelAzimuth",len(TgtSenRelAzimuth)
        # print "TgtSenRelElevation",len(TgtSenRelElevation)
        #print "Range",Range
        # print "PlyId",len(PlyId)
        # print "PixLocX",len(PixLocX)
        # print "PixLocY",len(PixLocY)
        # print "Aspect",len(Aspect)
        # print "TgtType",len(TgtType)
        Frame = range(1,len(Time)+1)
        VideoName = [VideoName[0] for i in range(len(Time))]
        data = {"VideoName":VideoName,"Frame":Frame,"Time":Time,"Speed":Speed,"VelStdDev":VelStdDev,"VelEast":VelEast,
                "VelNorth":VelNorth,"VelUp":VelUp,"SlantRange":SlantRange,"Heading":Heading,
                "TgtSenRelAzimuth":TgtSenRelAzimuth,"TgtSenRelElevation":TgtSenRelElevation,"PlyId":PlyId,"PixLocX":PixLocX,
                "PixLocY": PixLocY,"Aspect": Aspect,"TgtType": TgtType,"Range":Range}
        data_frame = DataFrame(dict([(k,Series(v)) for k,v in data.iteritems()]))
        csv_name = fileOnlyName + ".csv"
       # csv_path = os.path.join(os.getcwd(),csv_name)
       # print os.getcwd()
        data_frame.to_csv(csv_name,index=False)

if __name__== "__main__":
    folderDir = "sample_data/AGT/Visible/"
    #folderDir = "/media/shuoliu/DATAPART1/Shuo/IROD/ATR_Database/sample_data/AGT/Visible_agt/"
   # folderDir = os.path.join(os.getcwd(),folderDir)   
    listDir = os.listdir(folderDir)
    print folderDir
    print listDir
    for f in listDir:
        if os.path.splitext(f)[1] ==".agt":
            filePath = folderDir + f
            paserFile(filePath)

    # paserFile("sample_data/IR_agt/cegr02003_0001.agt")

