import cv2
from pandas import Series,DataFrame
import pandas
import numpy as np

image_dir = "sample_data/Imagery/Visible/images/i1co02003_0001_1.png"

im = cv2.imread(image_dir)

print im