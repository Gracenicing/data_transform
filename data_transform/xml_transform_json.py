# -*- coding: utf-8 -*-
import os
import sys
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
import json
import cv2
import io
import base64
from xml.dom.minidom import Document

def create_xml_anno():
    doc = Document()  #创建DOM文档对象
    DOCUMENT = doc.createElement('annotation') #创建根元素
    
    floder  = doc.createElement('floder')          ##建立自己的开头
    floder_text  = doc.createTextNode('JPEGImages')##建立自己的文本信息 
    floder.appendChild(floder_text)                ##自己的内容
    DOCUMENT.appendChild(floder)                   
    doc.appendChild(DOCUMENT)
    
    filename  = doc.createElement('filename')           
    filename_text  = doc.createTextNode('00000.jpg') 
    filename.appendChild(filename_text)               
    DOCUMENT.appendChild(filename)                   
    doc.appendChild(DOCUMENT)
    
    path  = doc.createElement('path')           
    path_text  = doc.createTextNode('/home/ubuntu/JPEGImages/000000.jpg') 
    path.appendChild(path_text)               
    DOCUMENT.appendChild(path)                   
    doc.appendChild(DOCUMENT)
    
    source  = doc.createElement('source') 
    database = doc.createElement('database')
    database_text = doc.createTextNode('Unknow') #元素内容写入
    database.appendChild(database_text)
    source.appendChild(database)                  
    DOCUMENT.appendChild(source)                   
    doc.appendChild(DOCUMENT)
    
    size  = doc.createElement('size') 
    width = doc.createElement('width')
    width_text = doc.createTextNode('1920') #元素内容写入
    width.appendChild(width_text)
    size.appendChild(width) 
    
    height = doc.createElement('height')
    height_text = doc.createTextNode('1080') 
    height.appendChild(height_text)
    size.appendChild(height)   
    
    depth = doc.createElement('depth')
    depth_text = doc.createTextNode('3') 
    depth.appendChild(depth_text)
    size.appendChild(depth) 
                
    DOCUMENT.appendChild(size) 
    
    segmented  = doc.createElement('segmented')           
    segmented_text  = doc.createTextNode('0') 
    segmented.appendChild(segmented_text)               
    DOCUMENT.appendChild(segmented)                   
    doc.appendChild(DOCUMENT) 
    
    object  = doc.createElement('object') 
    name = doc.createElement('name')
    name_text = doc.createTextNode('B')
    name.appendChild(name_text)
    object.appendChild(name) 
    
    pose = doc.createElement('pose')
    pose_text = doc.createTextNode('Unspecified') 
    pose.appendChild(pose_text)
    object.appendChild(pose)   
    
    truncated = doc.createElement('truncated')
    truncated_text = doc.createTextNode('0') 
    truncated.appendChild(truncated_text)
    object.appendChild(truncated) 
    
    bndbox  = doc.createElement('bndbox') 
    xmin = doc.createElement('xmin')
    xmin_text = doc.createTextNode('342')
    xmin.appendChild(xmin_text)
    bndbox.appendChild(xmin) 
    
    ymin = doc.createElement('ymin')
    ymin_text = doc.createTextNode('330') 
    ymin.appendChild(ymin_text)
    bndbox.appendChild(ymin)   
    
    xmax = doc.createElement('xmax')
    xmax_text = doc.createTextNode('581')
    xmax.appendChild(xmax_text)
    bndbox.appendChild(xmax) 
    
    ymax = doc.createElement('ymax')
    ymax_text = doc.createTextNode('753') 
    ymax.appendChild(ymax_text)
    bndbox.appendChild(ymax) 
    object.appendChild(bndbox)
    
    DOCUMENT.appendChild(object) 
    
    object  = doc.createElement('object') 
    name = doc.createElement('name')
    name_text = doc.createTextNode('B')
    name.appendChild(name_text)
    object.appendChild(name) 
    
    pose = doc.createElement('pose')
    pose_text = doc.createTextNode('Unspecified') 
    pose.appendChild(pose_text)
    object.appendChild(pose)   
    
    truncated = doc.createElement('truncated')
    truncated_text = doc.createTextNode('0') 
    truncated.appendChild(truncated_text)
    object.appendChild(truncated) 
    
    bndbox  = doc.createElement('bndbox') 
    xmin = doc.createElement('xmin')
    xmin_text = doc.createTextNode('342')
    xmin.appendChild(xmin_text)
    bndbox.appendChild(xmin) 
    
    ymin = doc.createElement('ymin')
    ymin_text = doc.createTextNode('330') 
    ymin.appendChild(ymin_text)
    bndbox.appendChild(ymin)   
    
    xmax = doc.createElement('xmax')
    xmax_text = doc.createTextNode('581')
    xmax.appendChild(xmax_text)
    bndbox.appendChild(xmax) 
    
    ymax = doc.createElement('ymax')
    ymax_text = doc.createTextNode('753') 
    ymax.appendChild(ymax_text)
    bndbox.appendChild(ymax) 
    object.appendChild(bndbox)
    
    DOCUMENT.appendChild(object) 
    ############item:Python处理XML之Minidom################
    
    ########### 将DOM对象doc写入文件
    f = open('aha.xml','w')
    
    doc.writexml(f,indent = '\t',newl = '\n', addindent = '\t',encoding='utf-8')
    f.close()

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