import os
import os.path as op
from pandas import Series,DataFrame
import pandas  as pd
import numpy as np
import time
ImgType = "IR_Reg"
Annotations_dir = op.join("sample_data/Annotations",ImgType)
if not os.path.exists(Annotations_dir):
    os.makedirs(Annotations_dir)
Train_Test_dir = op.join("sample_data/Train_Test",ImgType)
if not os.path.exists(Train_Test_dir):
    os.makedirs(Train_Test_dir)

GT_file = op.join("sample_data/GroundTruth","Visible","FullList.csv")

if not os.path.isfile(GT_file):
    print "no that file"
else:
    df = pd.read_csv(GT_file,na_values=['-1',' '])
    clean_df = df[pd.notnull(df['Match'])]
    train_df = clean_df[(clean_df["TgtType"]!="ZSU23") & (clean_df["TgtType"]!="2S3")]
    train_df = train_df[train_df["Frame"]%5 == 0] # skip 5 frame
    test_df = clean_df[(clean_df["TgtType"]=="ZSU23") | (clean_df["TgtType"]=="2S3")]
    test_df = test_df[test_df["Frame"]%5==0]
    train_df = train_df.reindex(np.random.permutation(train_df.index))
    #test_df = test_df.reindex(np.random.permutation(test_df.index))
    train_image = train_df["Match"]
    train_box= DataFrame({"X1":train_df['UpperLeft'],"Y1":train_df["UpperTop"],"X2":train_df["UpperLeft"]
                     +train_df["BBoxW"],"Y2":train_df["UpperTop"]+train_df["BBoxH"]},columns=["X1","Y1","X2","Y2"])
    test_image = test_df["Match"]
    test_box= DataFrame({"X1":test_df['UpperLeft'],"Y1":test_df["UpperTop"],"X2":test_df["UpperLeft"]
                     +test_df["BBoxW"],"Y2":test_df["UpperTop"]+test_df["BBoxH"]},columns=["X1","Y1","X2","Y2"])
    train_image.to_csv(op.join(Train_Test_dir,"train.txt"),index=False,header=False)
    train_box.to_csv(op.join(Annotations_dir,"train.txt"),index=False,header=False)

    test_image.to_csv(op.join(Train_Test_dir,"test.txt"),index=False,header=False)
    test_box.to_csv(op.join(Annotations_dir,"test.txt"),index=False,header=False)

    # cls_df = clean_df["TgtType"]
    # for i in range(len(cls_df)):
    #     if cls_df[i] ==
    # print cls_df
    # print len(box_df)
    # print len(image_df)
