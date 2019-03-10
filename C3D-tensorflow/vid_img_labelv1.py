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
import math

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
    event_len_covered_dict = {}
    event_len_dict = {}
    event_log_val_dict = {}
    event_next_step_dict = {}
    class_buckets = {}
    while cap.isOpened():
            ret, frame = cap.read()
            for clss, action_list in enumerate(data['tlabs']):
                for dummy in action_list:
                    for action_item_no, action in enumerate(dummy):

                        if action[0] <= fidx <= action[1]:
                            dict_key = "{}_{}_{}".format(clss, input_video_file_name, action_item_no)
                            event_len = action[1] - action[0]
                            base_path = get_full_path("{}/{}/{}/{}/".format(OUTPUT, clss, input_video_file_name, action_item_no))
                            if clss in [3,4]:
                                if event_len > 32 and event_len % 32 > 0:
                                    class_buckets[dict_key] = class_buckets.get(dict_key, {'current_bucket': 0, 'bucket_len': 0})
                                    total_bucket = int(event_len % 32)
                                    dict_key = "{}_{}_{}_{}".format(clss, input_video_file_name, action_item_no, class_buckets[dict_key]['current_bucket'])
                                    base_path = "{}/{}/".format(base_path, class_buckets[dict_key]['current_bucket'])
                                    class_buckets[dict_key]['bucket_len'] += 1
                                    if class_buckets[dict_key]['bucket_len'] >= 32:
                                        class_buckets[dict_key]['current_bucket'] += 1
                                        class_buckets[dict_key]['bucket_len'] = 0
                            try:
                                os.makedirs(base_path)
                            except Exception:
                                pass

                            event_len_dict[dict_key] = event_len_dict.get(dict_key, event_len) # waste of compute
                            if event_len > 16:
                                event_log_val_dict[dict_key] = event_log_val_dict.get(dict_key, math.floor(math.log(event_len/16, 2))) # waste of compute
                            else:
                                event_log_val_dict[dict_key] = 0
                            event_next_step_dict[dict_key] = event_next_step_dict.get(dict_key, action[0])
                            event_len_covered_dict[dict_key] = event_len_covered_dict.get(dict_key, 0)

                            expected_steps = 2**event_log_val_dict[dict_key]
                            if event_len_covered_dict[dict_key] <= expected_steps: # till we reach the sub-sample limit
                                if event_next_step_dict[dict_key] == fidx:
                                    event_next_step_dict[dict_key] += event_log_val_dict[dict_key] # next step
                                    event_len_covered_dict[dict_key] = fidx - action[0]
                                    # do something
                                    do_something(image, clss, input_video_file_name, action_item_no, dict_key, fidx)
                            else:
                                # do something
                                do_something(image, clss, input_video_file_name, action_item_no, dict_key, fidx)
            fidx += 1
            if not ret:
                break
    cap.release()


def do_something(image, base_path, dict_key, fidx, ):
    file_name = "{}_{}".format(dict_key, fidx)
    file_path = "{}/{}".format(base_path, file_name)
    resize = cv2.resize(image, (320, 240), interpolation = cv2.INTER_LINEAR)
    cv2.imwrite("{}.jpg".format(file_path), resize)
    file_path = base_path[:-1]
    list_file.write("{} {}\n".format(file_path, clss))


if __name__ == "__main__":
    t1 = time.time()
    print "Start time {}".format(t1)
    main()
    t2 = time.time()
    print "Time taken {}".format(t2-t1)
