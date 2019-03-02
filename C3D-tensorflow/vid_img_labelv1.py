# coding: utf-8
import scipy.io
import os
from contextlib import closing
from videosequence import VideoSequence

BASE = "."
LABEL = "Labels_MERL_Shopping_Dataset"
VIDEO = "Videos_MERL_Shopping_Dataset"
OUTPUT = "output"
LIST = "list"

def get_full_path(filename, seed="", ext=""):
    return "{}/{}/{}{}".format(BASE, seed, filename, ext)


def main():
    with open(get_full_path(LIST, "train", ".list")) as train_file, open(get_full_path(LIST, "test", ".list")) as test_file:
        for idx, label_name in enumerate(os.listdir(get_full_path(LABEL))):
            item, _ = label_name.split("label")
            video_clip_name = "{}_crop".format(item)
            target_file = train_file
            if idx % 4 == 0:
                target_file = test_file
            getstartstop(video_clip_name, label_name, target_file)


def getstartstop(input_video_file_name, input_label_file_name, list_file):
    input_label_file = get_full_path(LABEL, input_label_file_name, ".mat")
    data = scipy.io.loadmat(input_label_file)
    video_file = get_full_path(VIDEO, input_video_file_name, ".mp4")
    with closing(VideoSequence(video_file)) as frames:
        for fidx, frame in enumerate(frames):
            for clss, action_list in enumurate(data['tlabs']):
                os.mkdir(get_full_path(OUTPUT, clss))
                for action in action_list:
                    if action[0] <= fidx <= action[1]:
                        file_name = "{}_{}_{}".format(clss, input_video_file_name, fidx)
                        file_path = get_full_path(OUTPUT, clss, file_name)
                        frame.save("{}.jpg".format(file_path)
                        target_file.write("{} {}".format(list_file, clss))