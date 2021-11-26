# """
# 将labelImg标记的xml文件转成labelme标记的json文件
# python main.py param1 param2 param3
# param1 : xml文件所在的文件夹的路径
# param2： 保存的json文件所在的文件夹路径
# param3:  原始图片的路径
# 例如：
# 命令行输入：
# python main.py C:\data_convert_tool\xml_transform_json\picture\xml C:\data_convert_tool\xml_transform_json\picture\json C:\data_convert_tool\xml_transform_json\picture\image
# """

import os
import sys
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
import json
import cv2
import io
import base64

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

def generate_json(file_dir,file_name, raw_image_path):
    str_json = {}
    shapes = []
    # 读取坐标
    bboxes = parse_xml(os.path.join(file_dir, file_name))
    for one_bbox in bboxes:
        label_name = one_bbox[-1]
        one_bbox = one_bbox[:-1]
        points = []
        points.append([float(one_bbox[0]),float(one_bbox[1])])
        points.append([float(one_bbox[2]),float(one_bbox[3])])
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
    picture_basename = file_name.replace('.xml', '.jpg')
    image_path = os.path.join(raw_image_path, picture_basename)
    image_path = image_path.replace("\\", "/")
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

def main(xml_path, json_path, raw_image_path):
    xml_path = xml_path.replace("\\", "/")
    json_path = json_path.replace("\\", "/")
    raw_image_path = raw_image_path.replace("\\", "/")
    path_xml = os.listdir(xml_path)
    for file_name in path_xml:
        str_json = generate_json(xml_path, file_name, raw_image_path)
        json_data = json.dumps(str_json)
        jsonfile_name = file_name.replace(".xml",".json")
        f = open(os.path.join(json_path, jsonfile_name), 'w')
        f.write(json_data)
        f.close()


# if __name__=="__main__":
#     xml_path = sys.argv[1]
#     json_path = sys.argv[2]
#     raw_image_path = sys.argv[3]
#     # xml_path = r'C:\data_convert_tool\xml_transform_json\picture\xml'
#     # json_path = r'C:\data_convert_tool\xml_transform_json\picture\json'
#     # raw_image_path = r'C:\data_convert_tool\xml_transform_json\picture\image'
#     main(xml_path, json_path, raw_image_path)