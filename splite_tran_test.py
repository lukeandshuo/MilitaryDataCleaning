import os
import os.path as op
from pandas import Series,DataFrame
import pandas  as pd
import numpy as np
import time
import cv2
skip_num = 5
IRImgType = "IR_Reg"
VImgType = "Visible"
IR_Annotations_dir = op.join("sample_data/Annotations",IRImgType)
if not os.path.exists(IR_Annotations_dir):
    os.makedirs(IR_Annotations_dir)
V_Annotations_dir = op.join("sample_data/Annotations",VImgType)
if not os.path.exists(V_Annotations_dir):
    os.makedirs(V_Annotations_dir)
IR_Image_Dir =op.join("sample_data/Imagery",IRImgType,"images")
V_Image_Dir = op.join("sample_data/Imagery",VImgType,"images")

IR_Motion_Dir = op.join("sample_data/Imagery/IR_Motion/images")
if not os.path.exists(IR_Motion_Dir):
    os.makedirs(IR_Motion_Dir)
V_Motion_Dir = op.join("sample_data/Imagery/V_Motion/images")
if not os.path.exists(V_Motion_Dir):
    os.makedirs(V_Motion_Dir)


IR_list_dir = op.join("sample_data/Train_Test",IRImgType)
if not os.path.exists(IR_list_dir):
    os.makedirs(IR_list_dir)
V_list_dir = op.join("sample_data/Train_Test",VImgType)
if not os.path.exists(V_list_dir):
    os.makedirs(V_list_dir)

# generate IR and Visible motion images
def GenerateMotion(df):
    df = df.reset_index()
    IR_Image_Dir = op.join("sample_data/Imagery", IRImgType, "images")
    V_Image_Dir = op.join("sample_data/Imagery", VImgType, "images")

    IR_Motion_Dir = op.join("sample_data/Imagery/IR_Motion/images")
    if not os.path.exists(IR_Motion_Dir):
        os.makedirs(IR_Motion_Dir)
    V_Motion_Dir = op.join("sample_data/Imagery/V_Motion/images")
    if not os.path.exists(V_Motion_Dir):
        os.makedirs(V_Motion_Dir)

    for i,name in enumerate(df['Match']):
        current_frame = i
        last_frame=max(i-1,0)

        #Generate IR motion images
        c_name = op.join(IR_Image_Dir,str(df['Match'][current_frame])+".png")
        c_image = cv2.imread(c_name)
        l_name = op.join(IR_Image_Dir,str(df['Match'][last_frame])+".png")
        l_image = cv2.imread(l_name)
        motion_image=cv2.absdiff(c_image,l_image)
        cv2.imwrite(op.join(IR_Motion_Dir,str(df['Match'][current_frame])+".png"),motion_image)

        #Generate Visible motion images
        c_name = op.join(V_Image_Dir,str(df['ImageName'][current_frame])+".png")
        c_image = cv2.imread(c_name)
        l_name = op.join(V_Image_Dir,str(df['ImageName'][last_frame])+".png")
        l_image = cv2.imread(l_name)
        motion_image=cv2.absdiff(c_image,l_image)
        cv2.imwrite(op.join(V_Motion_Dir,str(df['ImageName'][current_frame])+".png"),motion_image)

# generate three channel images
def Generate3CImg(df):
    df = df.reset_index()
    IR_Image_Dir = op.join("sample_data/Imagery", IRImgType, "images")
    V_Image_Dir = op.join("sample_data/Imagery", VImgType, "images")
    V_Motion_Dir = op.join("sample_data/Imagery/V_Motion/images")
    ThreeC_Image_Dir = op.join("sample_data/Imagery/3C/images")
    if  not op.exists(ThreeC_Image_Dir):
        os.makedirs(ThreeC_Image_Dir)
    for i, name in enumerate(df['ImageName']):
        v_name = op.join(V_Image_Dir,str(name)+".png")
        v_image = cv2.imread(v_name,0) # load image in gray scale
        ir_name = op.join(IR_Image_Dir,str(df['Match'][i]+".png"))
        ir_image = cv2.imread(ir_name,0)
        m_name = op.join(V_Motion_Dir,str(name)+".png")
        print m_name
        m_image= cv2.imread(m_name,0)

        image = cv2.merge((v_image,m_image,ir_image))    #merge
       # image = np.concatenate((v_image,ir_image,m_image),1) #split
       #  cv2.imshow("result",image)
       #  cv2.waitKey(20)

        threeC_name = op.join(ThreeC_Image_Dir,str(name)+".png")
        cv2.imwrite(threeC_name,image)



GT_file = op.join("sample_data/GroundTruth","Visible","FullList.csv")
if not os.path.isfile(GT_file):
    print "no that file"
else:
    df = pd.read_csv(GT_file,na_values=['-1',' '])
    clean_df = df[pd.notnull(df['Match'])]
    train_df = clean_df[(clean_df["TgtType"]!="ZSU23") & (clean_df["TgtType"]!="2S3")& (clean_df["TgtType"]!="SUV")]
    train_df = train_df[train_df["Frame"]%skip_num == 0] # skip 5 frame
# GenerateMotion(train_df)
    Generate3CImg(train_df)
    test_df = clean_df[(clean_df["TgtType"]=="ZSU23") | (clean_df["TgtType"]=="2S3")| (clean_df["TgtType"]=="SUV")]
    test_df = test_df[test_df["Frame"]%skip_num==0]

   # GenerateMotion(test_df)
    Generate3CImg(test_df)

    # train_df = train_df.reindex(np.random.permutation(train_df.index))
    # #test_df = test_df.reindex(np.random.permutation(test_df.index))
    # print len(test_df['TgtType'])
    # print len(train_df['TgtType'])
    # IR_train_image = train_df["Match"]
    # V_train_image = train_df['ImageName']
    # train_box= DataFrame({"X1":train_df['UpperLeft'],"Y1":train_df["UpperTop"],"X2":train_df["UpperLeft"]
    #                  +train_df["BBoxW"],"Y2":train_df["UpperTop"]+train_df["BBoxH"]},columns=["X1","Y1","X2","Y2"])
    # IR_test_image = test_df["Match"]
    # V_test_image = test_df['ImageName']
    # test_box= DataFrame({"X1":test_df['UpperLeft'],"Y1":test_df["UpperTop"],"X2":test_df["UpperLeft"]
    #                  +test_df["BBoxW"],"Y2":test_df["UpperTop"]+test_df["BBoxH"]},columns=["X1","Y1","X2","Y2"])
    #
    # IR_train_image.to_csv(op.join(IR_list_dir,"train.txt"),index=False,header=False)
    # train_box.to_csv(op.join(IR_Annotations_dir,"train.txt"),index=False,header=False)
    #
    # IR_test_image.to_csv(op.join(IR_list_dir,"test.txt"),index=False,header=False)
    # test_box.to_csv(op.join(IR_Annotations_dir,"test.txt"),index=False,header=False)
    #
    # V_train_image.to_csv(op.join(V_list_dir,"train.txt"),index=False,header=False)
    # train_box.to_csv(op.join(V_Annotations_dir,"train.txt"),index=False,header=False)
    #
    # V_test_image.to_csv(op.join(V_list_dir,"test.txt"),index=False,header=False)
    # test_box.to_csv(op.join(V_Annotations_dir,"test.txt"),index=False,header=False)

