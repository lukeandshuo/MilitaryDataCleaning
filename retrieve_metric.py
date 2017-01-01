from numpy.ma.core import _DomainSafeDivide
import pandas
from pandas import DataFrame, Series
import os
IR_H = 512
IR_W = 640
V_H = 480
V_W = 640
MetricDir = "sample_data/Metric/"
IRMetricDir = MetricDir + "IR/"
<<<<<<< HEAD
VisibleMetricDir = MetricDir + "Visible"
=======
VisibleMetricDir = MetricDir + "Visible/"
>>>>>>> 474d68ab29d68cb47ad27b91e2b10cd2327211d4

AGTDir = "sample_data/AGT/"
IRAGTDir = AGTDir+"IR/"
VisibleAGTDir = AGTDir + "Visible/"

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
    return "-1"

IRMfile = os.listdir(IRMetricDir)

IRagtFile = os.listdir(IRAGTDir)
VagtFile =  os.listdir(VisibleAGTDir)
print IRagtFile
print VagtFile
for i,f in enumerate(IRMfile):
    if os.path.splitext(f)[1] == ".csv" and int(os.path.splitext(f)[0][5:9])>2000:
        print "num:"+ str(os.path.splitext(f)[0][5:9])
        print "file name:",f
        df_IRM = pandas.read_csv(IRMetricDir+f)
        df_IRagt = pandas.read_csv(IRAGTDir+f)
        df_Vagt = pandas.read_csv(VisibleAGTDir+SearchName(f,VagtFile))
        if df_Vagt['TgtType'][0]== "MAN":
            print df_Vagt['Time'][0]
            continue
        IR = DataFrame({'VideoName':df_IRagt['VideoName'],'Frame':df_IRagt["Frame"],"Time":df_IRagt['Time'],"X2":df_IRagt['PixLocX'],"Y2":df_IRagt['PixLocY'],"X1":df_IRM['UpperLeft'],"Y1":df_IRM['UpperTop']})
        Visible = DataFrame({'Frame':df_Vagt['Frame'],'Time':df_Vagt['Time'],'X2':df_Vagt['PixLocX'],'Y2':df_Vagt['PixLocY']})
        print Visible['Time'][0]
        print IR['Time'][0]
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
                if j < len(IR['Frame']):
                    X1 = Visible['X2'][i]-(float(IR['X2'][j]-IR['X1'][j])/float(IR_W))*V_W
                    V_X1.append(int(X1))
                    Y1 = Visible['Y2'][i]-(float(IR['Y2'][j]-IR['Y1'][j])/float(IR_H))*V_H
                    V_Y1.append(int(Y1))
                    # print IR['VideoName'][j]
                    # print IR['Frame'][j]
                    MatchName = str(IR['VideoName'][j])+"_"+str(IR['Frame'][j])
                    # print MatchName
                    Match.append(MatchName)
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
        W = (Visible['X2']-X1)*2
        H = (Visible['Y2']-Y1)*2
        Pot = H*W
        VisibleMetric = DataFrame({"VideoName":df_Vagt['VideoName'],"Frame":df_Vagt['Frame'],"Pot":Pot,"UpperLeft":X1,"UpperTop":Y1,"Match":Match})

        Name = VisibleMetricDir+df_Vagt['VideoName'][0]+".csv"
        VisibleMetric.to_csv(Name,index=False)