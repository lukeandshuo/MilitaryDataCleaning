import os
import os.path as op
import pandas
from pandas import Series,DataFrame
IRDir = "sample_data/GroundTruth/IR/"
VisibleDir = "sample_data/GroundTruth/Visible/"


def CombineFiles(Dir):
    First = True;
    FullFileName = "FullList.csv"
    files = os.listdir(Dir)
    for f in files:
        if os.path.splitext(f)[1] == ".csv" and f != "FullList.csv":
            df_data = pandas.read_csv(op.join(Dir,f))
            print "df_data",op.join(Dir,f)
            if First:
                with open(op.join(Dir,FullFileName),'w') as out:
                    df_data.to_csv(out,header=True,index=False)
                    First = False
            else:
                with open(op.join(Dir,FullFileName),'a') as out:
                    df_data.to_csv(out,header=False,index=False)

if __name__=="__main__":
    CombineFiles(IRDir)
    CombineFiles(VisibleDir)