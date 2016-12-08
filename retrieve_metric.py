from pandas import Series,DataFrame
import pandas
import os
IR_H = 512
IR_W = 640
V_H = 480
V_W = 640
MetricDir = "sample_data/Metric/"
IRMetricDir = MetricDir + "IR/"
VisibleMetricDir = MetricDir + "Visible/"

AGTDir = "sample_data/AGT/"
IRAGTDir = AGTDir+"IR_agt/"
VisibleAGTDir = AGTDir + "Visible_agt/"

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

IRMfile = os.listdir(IRMetricDir)

IRagtFile = os.listdir(IRAGTDir)
VagtFile =  os.listdir(VisibleAGTDir)

for i,f in enumerate(IRMfile):
    if os.path.splitext(f)[1] == ".csv":
        print f
        df_IRM = pandas.read_csv(IRMetricDir+f)
        df_IRagt = pandas.read_csv(IRAGTDir+f)
        df_Vagt = pandas.read_csv(VisibleAGTDir+VagtFile[i])

        IR = DataFrame({'Frame':df_IRagt["Frame"],"Time":df_IRagt['Time'],"X2":df_IRagt['PixLocX'],"Y2":df_IRagt['PixLocY'],"X1":df_IRM['UpperLeft'],"Y1":df_IRM['UpperTop']})
        Visible = DataFrame({'Frame':df_Vagt['Frame'],'Time':df_Vagt['Time'],'X2':df_Vagt['PixLocX'],'Y2':df_Vagt['PixLocY']})
        print GetTime(IR['Time'][0])
        IR_start = 0
        V_start = 0
        IR_t = GetTime(IR['Time'][0])
        V_t = GetTime(Visible['Time'][0])
        if IR_t > V_t:
            V_start = GetMatchIndex(Visible['Time'],IR_t)
        else:
            IR_start = GetMatchIndex(IR['Time'],V_t)

        print IR_start,V_start
        print IR['Time'][IR_start],Visible['Time'][V_start]

        V_X1 = []
        V_Y1 = []
        increment = 0
        for i in range(len(Visible['Frame'])):
            if i < V_start:
                V_X1.append(-1)
                V_Y1.append(-1)
            else:
                j = IR_start+increment
                if j < len(IR['Frame']):
                    X1 = Visible['X2'][i]-(float(IR['X2'][j]-IR['X1'][j])/float(IR_W))*V_W
                    V_X1.append(int(X1))
                    Y1 = Visible['Y2'][i]-(float(IR['Y2'][j]-IR['Y1'][j])/float(IR_H))*V_H
                    V_Y1.append(int(Y1))
                else:
                    V_X1.append(-1)
                    V_Y1.append(-1)
                increment += 1
        X1=Series(V_X1)
        Y1=Series(V_Y1)
        W = (Visible['X2']-X1)*2
        H = (Visible['Y2']-Y1)*2
        Pot = H*W
        VisibleMetric = DataFrame({"VideoName":df_Vagt['VideoName'],"Frame":df_Vagt['Frame'],"Pot":Pot,"UpperLeft":X1,"UpperTop":Y1})

        Name = VisibleMetricDir+df_Vagt['VideoName'][0]+".csv"
        VisibleMetric.to_csv(Name,index=False)