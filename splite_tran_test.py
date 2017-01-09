import os
import os.path as op
from pandas import Series,DataFrame
import pandas  as pd
import numpy as np
import time
IRImgType = "IR_Reg"
VImgType = "Visible"
IR_Annotations_dir = op.join("sample_data/Annotations",IRImgType)
if not os.path.exists(IR_Annotations_dir):
    os.makedirs(IR_Annotations_dir)
V_Annotations_dir = op.join("sample_data/Annotations",VImgType)
if not os.path.exists(V_Annotations_dir):
    os.makedirs(V_Annotations_dir)

IR_list_dir = op.join("sample_data/Train_Test",IRImgType)
if not os.path.exists(IR_list_dir):
    os.makedirs(IR_list_dir)
V_list_dir = op.join("sample_data/Train_Test",VImgType)
if not os.path.exists(V_list_dir):
    os.makedirs(V_list_dir)

GT_file = op.join("sample_data/GroundTruth","Visible","FullList.csv")

if not os.path.isfile(GT_file):
    print "no that file"
else:
    df = pd.read_csv(GT_file,na_values=['-1',' '])
    clean_df = df[pd.notnull(df['Match'])]
    train_df = clean_df[(clean_df["TgtType"]!="ZSU23") & (clean_df["TgtType"]!="2S3")& (clean_df["TgtType"]!="SUV")]
    train_df = train_df[train_df["Frame"]%5 == 0] # skip 5 frame
    test_df = clean_df[(clean_df["TgtType"]=="ZSU23") | (clean_df["TgtType"]=="2S3")| (clean_df["TgtType"]=="SUV")]
    test_df = test_df[test_df["Frame"]%5==0]
    train_df = train_df.reindex(np.random.permutation(train_df.index))
    #test_df = test_df.reindex(np.random.permutation(test_df.index))
    print len(test_df['TgtType'])
    print len(train_df['TgtType'])
    IR_train_image = train_df["Match"]
    V_train_image = train_df['ImageName']
    train_box= DataFrame({"X1":train_df['UpperLeft'],"Y1":train_df["UpperTop"],"X2":train_df["UpperLeft"]
                     +train_df["BBoxW"],"Y2":train_df["UpperTop"]+train_df["BBoxH"]},columns=["X1","Y1","X2","Y2"])
    IR_test_image = test_df["Match"]
    V_test_image = test_df['ImageName']
    test_box= DataFrame({"X1":test_df['UpperLeft'],"Y1":test_df["UpperTop"],"X2":test_df["UpperLeft"]
                     +test_df["BBoxW"],"Y2":test_df["UpperTop"]+test_df["BBoxH"]},columns=["X1","Y1","X2","Y2"])

    IR_train_image.to_csv(op.join(IR_list_dir,"train.txt"),index=False,header=False)
    train_box.to_csv(op.join(IR_Annotations_dir,"train.txt"),index=False,header=False)

    IR_test_image.to_csv(op.join(IR_list_dir,"test.txt"),index=False,header=False)
    test_box.to_csv(op.join(IR_Annotations_dir,"test.txt"),index=False,header=False)

    V_train_image.to_csv(op.join(V_list_dir,"train.txt"),index=False,header=False)
    train_box.to_csv(op.join(V_Annotations_dir,"train.txt"),index=False,header=False)

    V_test_image.to_csv(op.join(V_list_dir,"test.txt"),index=False,header=False)
    test_box.to_csv(op.join(V_Annotations_dir,"test.txt"),index=False,header=False)

    # cls_df = clean_df["TgtType"]
    # for i in range(len(cls_df)):
    #     if cls_df[i] ==
    # print cls_df
    # print len(box_df)
    # print len(image_df)
