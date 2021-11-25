# -*- coding: utf-8 -*-
import os
import json
import numpy as np
import sys
from tqdm import tqdm

def get_all_class(json_path):
    class_list = []
    path_json = os.listdir(json_path)
    for one_json in path_json:
        path = os.path.join(json_path, one_json)
        path = path.replace("\\", '/')
        with open(path,'r', encoding='utf-8') as path_json:
            jsonx = json.load(path_json)
            for shape in jsonx['shapes']:
                    label=str(shape['label'])
                    class_list.append(label)
    new_class_list = []
    [new_class_list.append(i) for i in class_list if i not in new_class_list]
    return new_class_list

def get_class_index(json_path, class_txt):
    new_class_list = get_all_class(json_path)
    if not os.path.exists(class_txt):
        os.makedirs(class_txt)
    class_txt = os.path.join(class_txt, "class_txt.txt")
    with open(class_txt, 'w') as f:
        dict_ = {}
        for index, one_class in enumerate(new_class_list):
            dict_[one_class] = index+1
        f.write(str(dict_))
        f.close()


def json_convert_txt(path_json, path_txt, class_dict):
    with open(path_json,'r', encoding='utf-8') as path_json:
        jsonx=json.load(path_json)

        with open(path_txt,'w+') as ftxt:
            for shape in jsonx['shapes']:
                xy=np.array(shape['points'])
                label=str(shape['label'])
                class_dict = eval(str(class_dict))
                label_index = str(class_dict[label])
                strxy = ''
                strxy+=label_index + " "
                for m,n in xy:
                    strxy+=str(m)+' '+str(n)+' '
                ftxt.writelines(strxy+"\n")


def main(dir_json, dir_txt, class_txt):
    if not os.path.exists(dir_txt):
        os.makedirs(dir_txt)

    class_txt = os.path.join(class_txt, "class_txt.txt")
    class_txt = class_txt.replace("\\", '/')
    with open(class_txt, 'r') as f:
        class_dict = f.readline()

    for json_name in tqdm(os.listdir(dir_json)):
        # print('cnt=%d,name=%s'%(cnt,json_name))
        path_json = os.path.join(dir_json, json_name)
        path_json = path_json.replace("\\", '/')
        path_txt = os.path.join(dir_txt, json_name.replace('.json','.txt'))
        path_txt = path_txt.replace("\\", '/')
        json_convert_txt(path_json, path_txt, class_dict)