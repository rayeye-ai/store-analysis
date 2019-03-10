# coding: utf-8
import scipy.io
import json
import os
import cv2
import time
import pprint

BASE = "."
LABEL = "Labels_MERL_Shopping_Dataset"
VIDEO = "Videos_MERL_Shopping_Dataset"
OUTPUT = "output"
LIST = "list"

def get_full_path(seed, filename="", ext=""):
    return "{}/{}/{}{}".format(BASE, seed, filename, ext)


master_dict = {0:{'item':[], 'avg_frame': 0}, 1:{'item':[], 'avg_frame': 0}, 2:{'item':[], 'avg_frame': 0}, 3:{'item':[], 'avg_frame': 0}, 4:{'item':[], 'avg_frame': 0,}}
for idx, label_name in enumerate(os.listdir(get_full_path(LABEL))):
    input_label_file = get_full_path(LABEL, label_name)
    data = scipy.io.loadmat(input_label_file)
    for clss, action_list in enumerate(data['tlabs']):

        #import ipdb; ipdb.set_trace()
        for actionl in action_list:
	    for action in actionl:
                act = {'start': str(action[0]), 'stop': str(action[1]), 'len': str(action[1]-action[0])}
                master_dict[clss]['item'].append(act)
		master_dict[clss]['avg_frame'] += action[1]-action[0]

for key, m in master_dict.iteritems():
	le = len(m['item'])
	m['avg_frame'] /= le

with open("chito", "w") as fop:
	fop.write(json.dumps(master_dict))

