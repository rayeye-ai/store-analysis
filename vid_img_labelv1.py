
# coding: utf-8

# In[ ]:


import numpy as np
import cv2
import scipy.io
import os

label_path="C:\\justin\\Videos_MERL_Shopping_Dataset\\Labels_MERL_Shopping_Dataset\\Labels_MERL_Shopping_Dataset\\"
label_file = open("label.list", "a")
output_path='C:\\justin\\Videos_MERL_Shopping_Dataset\\Data\\'
input_video_path='C:\\justin\\Videos_MERL_Shopping_Dataset\\Videos_MERL_Shopping_Dataset\\'
label_folder=os.listdir('C:\\justin\\Videos_MERL_Shopping_Dataset\\Labels_MERL_Shopping_Dataset\\Labels_MERL_Shopping_Dataset\\')
video_folder=os.listdir('C:\\justin\\Videos_MERL_Shopping_Dataset\\Videos_MERL_Shopping_Dataset')
print(label_folder[105])


# In[ ]:


i=0
for i in  range(0,len(label_folder)-1):
    input_video_file_name=video_folder[i]
    input_label_file_name=label_folder[i]
    print (input_video_file_name,input_label_file_name)
    getstartstop(input_video_file_name,input_label_file_name)
    i+=1


# In[ ]:


def getstartstop(input_video_file_name,input_label_file_name):
    input_label_file=label_path+input_label_file_name
    data = scipy.io.loadmat(input_label_file)
    for key, value in data.items():
        if key =='tlabs':
            d=np.array(value)
            tag=0
            while(tag<5):
                y=0
                j=0
                startstop_pos=[]
                while(y<len(d[tag][0])):
                    start,stop=d[tag][0][y]
                    vid2frame(input_video_file_name,start,stop,tag,y)
                    label_file.write(output_path+input_video_file+"_"+format(tag)+"_"+format(y)+" " + format(tag)+"/n")
                    y+=1
                tag+=1
    return


# In[ ]:


def vid2frame(input_video_file_name,start,stop,tag,y):
    
    input_video_file=input_video_path+input_video_file_name
    #output_path='C:\\justin\\Videos_MERL_Shopping_Dataset\\Data\\'
    output_folder=output_path+input_video_file_name[:-4]+"_"+format(tag)+"_"+format(y)
    os.mkdir(output_folder)
    vidcap = cv2.VideoCapture(input_video_file)
    success,image = vidcap.read()
    count = 0
    success = True
    while success:
        success,image = vidcap.read()
        if count>=start and count<=stop:
            filename=output_folder+"\\%d.jpg"%count
            print (filename)
            cv2.imwrite(filename, image)     # save frame as JPEG file
            
        count+=1
    
    vidcap.release()
    return

