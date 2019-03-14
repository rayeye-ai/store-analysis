# coding: utf-8
"""
The labels are formatted as below -

0 [array([[ 236,  257],
       [ 649,  685],
       [ 980, 1008],
       [1308, 1330],
       [1712, 1735],
       [2168, 2186],
       [2284, 2296],
       [2376, 2394],
       [2703, 2730],
       [3046, 3073],
       [3408, 3426],
       [ 561,  601],
       [2323, 2355]], dtype=uint16)]
1 [array([[ 606,  627],
       [2357, 2373],
       [ 257,  291],
       [ 686,  760],
       [1010, 1050],
       [1331, 1387],
       [1771, 1793],
       [2187, 2211],
       [2298, 2320],
       [2396, 2417],
       [2731, 2777],
       [3073, 3104],
       [3361, 3406],
       [3427, 3488]], dtype=uint16)]
2 [array([[1737, 1765]], dtype=uint16)]
3 [array([[ 300,  526],
       [ 765,  850],
       [1053, 1151],
       [1392, 1568],
       [2217, 2267],
       [2419, 2583],
       [2779, 2909],
       [3104, 3360],
       [3489, 3578]], dtype=uint16)]
4 [array([[ 178,  230],
       [ 865,  965],
       [1167, 1298],
       [1580, 1703],
       [2597, 2704],
       [2926, 3046]], dtype=uint16)]
"""


import scipy.io
import os
import cv2
import time

BASE = "."
LABEL = "Labels_MERL_Shopping_Dataset"
VIDEO = "Videos_MERL_Shopping_Dataset"
OUTPUT = "output"
SIZE = (1114, 680)
LIST = "list"
FPS = 20
print FPS


def get_full_path(seed, filename="", ext=""):
    return "{}/{}/{}{}".format(BASE, seed, filename, ext)


def main():
    with open(get_full_path(LIST, "train01", ".txt"), "w") as train_file:
        with open(get_full_path(LIST, "test01", ".txt"), "w") as test_file:
            for idx, label_name in enumerate(os.listdir(get_full_path(LABEL))):
                target_file = train_file
                if idx % 4 == 0:
                 target_file = test_file
                getstorage(label_name, target_file)
    cv2.destroyAllWindows()


def getstorage(label_name, target_file):
  input_label_file = get_full_path(LABEL, label_name)
  data = scipy.io.loadmat(input_label_file)
  super_dict = {}
  for clss, dummy in enumerate(data['tlabs']):
    for action_list in dummy:
      if clss in [3, 4]:
        action_list = perform_splits_sam(action_list)
      sampled_frames_list = perform_sub_sam(action_list)
    super_dict[clss] = sampled_frames_list
  write_to_files(super_dict, label_name, target_file)


def perform_splits_sam(action_list):
  res = []
  for action in action_list:
    start = action[0]
    end = action[1]
    frame_list = [frame for frame in xrange(start, end)]
    all_frame_list = [frame_list[i:i + 64] for i in xrange(0, len(frame_list), 64)]
    for fl in all_frame_list:
      res.append([fl[0], fl[-1]])
  return res


def perform_sub_sam(action_list):
  sampled_frames_list = []
  for action in action_list:
    start = action[0]
    end = action[1]
    frame_list = [frame for frame in xrange(start, end)]
    sampled_frames_list.append(frame_list)
  return sampled_frames_list


def write_to_files(super_dict, label_name, target_file):
  item, _ = label_name.split("label")
  input_video_file_name = "{}crop".format(item)
  input_label_file = get_full_path(LABEL, label_name)
  video_file = get_full_path(VIDEO, input_video_file_name, ".mp4")
  cap = cv2.VideoCapture(video_file)
  fidx = 0
  list_file = set()
  writer_dict = {}
  while cap.isOpened():
    ret, frame = cap.read()
    for clss, sampled_frames_list in super_dict.iteritems():
      for event_num, sample_frames in enumerate(sampled_frames_list):
        if fidx in sample_frames:
          file_name = "{}{}.avi".format(item, event_num)
          base_path = get_full_path("{}/{}".format(OUTPUT, clss))
          video_writer_name = "{}{}".format(clss, file_name)
          file_full_path = "{}{}".format(base_path, file_name)
          try:
            os.makedirs(base_path)
          except Exception:
            pass
          writer_dict[video_writer_name] = writer_dict.get(video_writer_name, cv2.VideoWriter(file_full_path, cv2.VideoWriter_fourcc(*'DIVX'), FPS, SIZE, True))
          frame = cv2.resize(frame, SIZE)
          writer_dict[video_writer_name].write(frame)
          #resize = cv2.resize(frame, (160, 120), interpolation = cv2.INTER_LINEAR)
          list_file.add("{}/{}".format(clss, file_name))
    fidx += 1
    if not ret:
      break
  for key in list_file:
    target_file.write("{}\n".format(key))
  cap.release()
  for name, writer in writer_dict.iteritems():
    print "closing writer {}".format(name)
    writer.release()


if __name__ == "__main__":
    t1 = time.time()
    print "Start time {}".format(t1)
    main()
    t2 = time.time()
    print "Time taken {}".format(t2-t1)
