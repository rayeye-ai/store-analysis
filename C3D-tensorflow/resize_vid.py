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
  item, _ = label_name.split("label")
  input_video_file_name = "{}crop".format(item)

  video_file = get_full_path(VIDEO, input_video_file_name, ".mp4")
  cap = cv2.VideoCapture(video_file)
  metadata_dict = {}

  for clss, data in enumerate(matlab_data['tlabs']):

    for action_list in data:
        start_end_dict = {}
        for idx, action in enumerate(action_list):
            if not os.path.exists(BASE + '/splits/' + str(clss)):
                os.makedirs(BASE + '/splits/' + str(clss))
            start_end_dict[action[0]] = action[1]


    metadata_dict[clss] = start_end_dict
  resize_by_start_end_frame(cap, metadata_dict, start_end_dict, input_video_file_name)
  cap.release()


size = 0
def resize_by_start_end_frame(cap, metadata_dict, start_end_dict, target_video_file):

    frame_count = 0
    frame_dict = {}   # format = {class: split_number: [frames]}
    split_count = 0
    end = 0
    global size
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if None in frame:
            break

        for clss in metadata_dict:

            # Print frame
            start_end_dict = metadata_dict[clss]
            print "frame count %s" % (frame_count)
            print "split count %s" % (split_count)

            if frame_count in start_end_dict:
                split_count += 1
                frame_dict[clss][split_count] = []
                end = start_end_dict[frame_count]

            if frame_count < end:
                frame_dict[clss][split_count].append(frame)

            frame_count += 1

#	if frame_count > 700:
#	    break


    if split_count == 0:
        return

    height, width, layers = frame_dict[0][1][0].shape
    size = (width, height)
    for clss in frame_dict:
        for count in clss:

            out_file = cv2.VideoWriter(BASE + "/splits" + str(clss) + "/" +  target_video_file + '_' + str(count) + '.avi', cv2.VideoWriter_fourcc(*'DIVX'), cv2.CAP_PROP_FPS, size)
            print "writing into file %s" % (target_video_file)
            for f in frame_dict[count]:
                out_file.write(f)
            out_file.release()

if __name__ == "__main__":
    main()
    print "done"
