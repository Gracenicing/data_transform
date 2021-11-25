# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import cv2
import numpy as np
import sys
import os
import json

from tqdm.std import tqdm


def parse_xml(src_label_path):
    et = ET.parse(src_label_path)
    element = et.getroot()
    element_objs = element.findall('object')
    bboxes = []
    for element_obj in element_objs:
        class_name = element_obj.find('name').text
        obj_bbox = element_obj.find('bndbox')
        xmin = int(round(float(obj_bbox.find('xmin').text)))
        ymin = int(round(float(obj_bbox.find('ymin').text)))
        xmax = int(round(float(obj_bbox.find('xmax').text)))
        ymax = int(round(float(obj_bbox.find('ymax').text)))
        bboxes.append([xmin, ymin, xmax, ymax, class_name])
    return bboxes


def get_all_class(xml_path):

    class_list = []
    path_xml = os.listdir(xml_path)
    
    for one_xml in path_xml:
        path = os.path.join(xml_path, one_xml)
        path = path.replace("\\", '/')
        et = ET.parse(path)
        element = et.getroot()
        element_objs = element.findall('object')
        for element_obj in element_objs:
            class_name = element_obj.find('name').text 
            class_list.append(class_name)

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


def main(xml_path, dir_txt, class_txt):
    if not os.path.exists(dir_txt):
        os.makedirs(dir_txt)
    class_txt = os.path.join(class_txt, "class_txt.txt")
    class_txt = class_txt.replace("\\", '/')
    with open(class_txt, 'r') as f:
        class_dict = f.readline()

    for json_name in tqdm(os.listdir(xml_path)):
        path_xml = os.path.join(xml_path, json_name)
        path_txt = os.path.join(dir_txt, json_name.replace('.xml','.txt'))
        with open(path_txt, "w+") as f:
            points = parse_xml(path_xml)
            for one_rect in points:
                class_dict = eval(str(class_dict))
                label_index = str(class_dict[str(one_rect[4])])
                f.writelines( label_index + " " + str(one_rect[0]) + " " + str(one_rect[1]) + " "+ str(one_rect[2]) + " " + str(one_rect[3])+"\n")