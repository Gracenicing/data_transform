# -*- coding: utf-8 -*-
import json
import base64
from PIL import Image
import io
import os
import cv2
import numpy as np
import sys
  
def generate_json(file_dir,file_name, raw_image_path):
    str_json = {}
    shapes = []
    # 读取坐标
    fr = open(os.path.join(file_dir, file_name))
    for line in fr.readlines():  # 逐行读取，滤除空格等
        # lineArr = line.strip().split(', ')
        lineArr = line.split(' ')
        label_name = str(lineArr[0])
        points = []
        points.append([float(lineArr[1]), float(lineArr[2])])
        points.append([float(lineArr[3]), float(lineArr[4])])
        shape = {}
        shape["label"] =  label_name
        shape["points"] = points
        shape["group_id"] = "null"
        shape["shape_type"] = "rectangle"
        shape["flags"] = {}
        shapes.append(shape)
    
    str_json["version"] = "4.6.0"
    str_json["flags"] = {}
    str_json["shapes"] = shapes
    # str_json["lineColor"] = [0, 255, 0, 128]
    # str_json["fillColor"] = [255, 0, 0, 128]
    picture_basename = file_name.replace('.txt', '.jpg')
    image_path = os.path.join(raw_image_path, picture_basename)
    image_path = image_path.replace('\\', '/')
    str_json["imagePath"] = picture_basename
    img = cv2.imread(image_path)
    str_json["imageHeight"] = img.shape[0]
    str_json["imageWidth"] = img.shape[1]
    str_json["imageData"] = base64encode_img(image_path)
    return str_json
 
def base64encode_img(image_path):
    src_image = Image.open(image_path)
    output_buffer = io.BytesIO()
    src_image.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode('utf-8')
    return base64_str
 
 
def main(file_dir, json_path, raw_image_path): 
    # file_dir = "C:\\txt_to_json"
    file_name_list = [file_name for file_name in os.listdir(file_dir) \
                            if file_name.lower().endswith('txt')]
    for file_name in file_name_list:
        str_json = generate_json(file_dir,file_name, raw_image_path)
        json_data = json.dumps(str_json)
        jsonfile_name = file_name.replace(".txt",".json")
        f = open(os.path.join(json_path, jsonfile_name), 'w')
        f.write(json_data)
        f.close()


if __name__ == "__main__":
    # txt_path = sys.argv[1]
    # json_path = sys.argv[2]
    # raw_image_path = sys.argv[3]
    txt_path = r"C:\data_convert_tool\txt_transform_json\picture\txt"
    json_path = r'C:\data_convert_tool\txt_transform_json\picture\json'
    raw_image_path = r'C:\data_convert_tool\txt_transform_json\picture\image'
    main(txt_path, json_path, raw_image_path)