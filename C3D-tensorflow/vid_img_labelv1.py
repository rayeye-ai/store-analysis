# coding: utf-8
import scipy.io
import os
import cv2
import time

BASE = "."
LABEL = "Labels_MERL_Shopping_Dataset"
VIDEO = "Videos_MERL_Shopping_Dataset"
OUTPUT = "output"
LIST = "list"

def get_full_path(seed, filename="", ext=""):
    return "{}/{}/{}{}".format(BASE, seed, filename, ext)


def main():
    with open(get_full_path(LIST, "train", ".list"), "w") as train_file, open(get_full_path(LIST, "test", ".list"), "w") as test_file:
        for idx, label_name in enumerate(os.listdir(get_full_path(LABEL))):
            item, _ = label_name.split("label")
            video_clip_name = "{}crop".format(item)
            target_file = train_file
            if idx % 4 == 0:
                target_file = test_file
            getstartstop(video_clip_name, label_name, target_file)
    cv2.destroyAllWindows()


def getstartstop(input_video_file_name, input_label_file_name, list_file):
    input_label_file = get_full_path(LABEL, input_label_file_name)
    data = scipy.io.loadmat(input_label_file)
    video_file = get_full_path(VIDEO, input_video_file_name, ".mp4")
    cap = cv2.VideoCapture(video_file)
    fidx = 0
    while cap.isOpened():
            ret, frame = cap.read()
            for clss, action_list in enumerate(data['tlabs']):
                try:
                    os.makedirs(get_full_path(OUTPUT, clss))
                except Exception:
                    pass
                for action in action_list[0]:
                    if action[0] <= fidx <= action[1]:
                        file_name = "{}_{}_{}".format(clss, input_video_file_name, fidx)
                        file_path = get_full_path("{}/{}".format(OUTPUT, clss), file_name)
                        cv2.imwrite("{}.jpg".format(file_path), frame)
                        list_file.write("{} {}\n".format(file_path, clss))
            fidx += 1
            if not ret:
                break
    cap.release()

if __name__ == "__main__":
    t1 = time.time()
    print "Start time {}".format(t1)
    main()
    t2 = time.time()
    print "Time taken {}".format(t2-t1)
