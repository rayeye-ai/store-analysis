# coding: utf-8
#This file contains utils to resize a video
import cv2
import scipy.io
import os

BASE = "."
LABEL = "Labels_MERL_Shopping_Dataset"
VIDEO = "Videos_MERL_Shopping_Dataset"
OUTPUT = "output"
LIST = "list"


def get_full_path(seed, filename="", ext=""):
    return "{}/{}/{}{}".format(BASE, seed, filename, ext)


def main():
    for idx, label_name in enumerate(os.listdir(get_full_path(LABEL))):
        getstorage(label_name)
    cv2.destroyAllWindows()


def getstorage(label_name):
  input_label_file = get_full_path(LABEL, label_name)
  matlab_data = scipy.io.loadmat(input_label_file)
  for clss, data in enumerate(matlab_data['tlabs']):
    item, _ = label_name.split("label")
    input_video_file_name = "{}crop".format(item)

    video_file = get_full_path(VIDEO, input_video_file_name, ".mp4")
    cap = cv2.VideoCapture(video_file)
    for action_list in data:
        for action in action_list:

            resize_by_start_end_frame(cap, action[0], action[1], clss + "/" + video_file, cap)



def resize_by_start_end_frame(cap, start, end, target_video_file, fps, size):

    frame_count = 0
    size = 0
    frame_list = []
    while True:
        ret, frame = cap.read()
        frame_count += 1

        if frame_count >= start:
            frame_list.append(frame)

        if frame_count == end:
            height, width, layers = frame.shape
            size = (width, height)
            break

    out_file = cv2.VideoWriter(target_video_file, cv2.VideoWriter_fourcc(*'DIVX'), cv2.CAP_PROP_FPS, size)
    for f in frame_list:
        out_file.write(f)
    out_file.release()
