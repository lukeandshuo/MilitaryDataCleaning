import os
import pandas
from pandas import Series,DataFrame

IRDir = "sample_data/GroundTruth/IR_GT/"
VisibleDir = "sample_data/GroundTruth/Visible_GT/"


def CombineFiles(Dir):
    First = True;
    FullFileName = "FullList.csv"
    files = os.listdir(Dir)
    for f in files:
        if os.path.splitext(f)[1] == ".csv":
            df_data = pandas.read_csv(Dir+f)
            if First:
                with open(Dir+FullFileName,'w') as out:
                    df_data.to_csv(out,header=True,index=False)
                    First = False
            else:
                with open(Dir+FullFileName,'a') as out:
                    df_data.to_csv(out,header=False,index=False)

if __name__=="__main__":
    CombineFiles(IRDir)
    CombineFiles(VisibleDir)