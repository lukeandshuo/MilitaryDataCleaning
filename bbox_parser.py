import os
import os.path as op
from pandas import Series, DataFrame
def paserBbox(path):
    fileOnlyName = os.path.splitext(path)[0]
    upper_left  = []
    upper_top = []
    pot = []
    video_name = []
    frame =[]
    with open(path,"r") as file:
        for words in file:
            words = words.strip("\n").split(",")
            frame.append(words[5])
            upper_left.append(words[9])
            upper_top.append(words[10])
            pot.append(words[13])
            video_name.append("".join(words[3:5]))
    print "frame",frame
    print "upper left",upper_left
    print "upper top", upper_top
    print "pot",pot
    print "Video Name",video_name
    data_dic = {"VideoName":video_name,"Frame":frame,"Pot":pot,"UpperLeft":upper_left,"UpperTop":upper_top}
    data_frame = DataFrame(dict([(k,Series(v)) for k,v in data_dic.iteritems()]))
    data_csv = data_frame.to_csv(index=False)
    file_csv = fileOnlyName + ".csv"
    with open(file_csv,'w') as file:
        file.write(data_csv)

if __name__ == "__main__":
    ImgType = "IR"
    pathDir = op.join("sample_data/Metric",ImgType)
    listDir = os.listdir(pathDir)
    print listDir
    for f in listDir:
        if os.path.splitext(f)[1] == '.bbox_met':
            filePath = op.join(pathDir , f)
            paserBbox(filePath)