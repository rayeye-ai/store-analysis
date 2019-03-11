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
LIST = "list"


def get_full_path(seed, filename="", ext=""):
    return "{}/{}/{}{}".format(BASE, seed, filename, ext)


def main():
    with open(get_full_path(LIST, "train", ".list"), "w") as train_file:
        with open(get_full_path(LIST, "test", ".list"), "w") as test_file:
            for idx, label_name in enumerate(os.listdir(get_full_path(LABEL))):
                target_file = train_file
                if idx % 4 == 0:
                 target_file = test_file
                getstorage(label_name, target_file)
    cv2.destroyAllWindows()


def getstorage(label_name, target_file):
  input_label_file = get_full_path(LABEL, label_name)
  data = scipy.io.loadmat(input_label_file)
  for clss, dummy in enumerate(data['tlabs']):
    for action_list in dummy:
      if clss in [3, 4]:
        action_list = perform_splits_sam(action_list)
      sampled_frames_list = perform_sub_sam(action_list)
    write_to_files(clss, sampled_frames_list, label_name, target_file)


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
    while True:
      if len(frame_list)/2 < 16:
        drop_out_list = []
        for idx, fram in enumerate(frame_list):
          if len(drop_out_list) + 16 <= len(frame_list):
            if idx%2 == 0:
              drop_out_list.append(fram)
          else:
            drop_out_list.append(fram)
        frame_list = drop_out_list
        break
      else:
        f_list = frame_list[0::2]
        if len(frame_list)%2 == 0:
          f_list.append(frame_list[-1])
        frame_list = f_list
    sampled_frames_list.append(frame_list)
  return sampled_frames_list


def write_to_files(clss, sampled_frames_list, label_name, target_file):
  item, _ = label_name.split("label")
  input_video_file_name = "{}crop".format(item)
  input_label_file = get_full_path(LABEL, label_name)
  video_file = get_full_path(VIDEO, input_video_file_name, ".mp4")
  cap = cv2.VideoCapture(video_file)
  fidx = 0
  list_file = {}
  while cap.isOpened():
    ret, frame = cap.read()
    for event_num, sample_frames in enumerate(sampled_frames_list):
      if fidx in sample_frames:
        base_path = get_full_path("{}/{}/{}".format(OUTPUT, clss, item), event_num)
        try:
          os.makedirs(base_path)
        except Exception:
          pass
        file_name = "{}_{}".format(input_video_file_name, fidx)
        file_path = "{}/{}".format(base_path, file_name)
        resize = cv2.resize(frame, (160, 120), interpolation = cv2.INTER_LINEAR)
        cv2.imwrite("{}.jpg".format(file_path), resize)
        list_file[base_path] = clss
    fidx += 1
    if not ret:
      break
  for key, val in list_file.iteritems():
    target_file.write("{} {}\n".format(key, val))
  cap.release()


if __name__ == "__main__":
    t1 = time.time()
    print "Start time {}".format(t1)
    main()
    t2 = time.time()
    print "Time taken {}".format(t2-t1)
