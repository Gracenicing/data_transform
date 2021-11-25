# -*- coding: utf-8 -*-
from xml.dom.minidom import Document
import sys
import os
import cv2


class CreateAnno:
    def __init__(self,):
        self.doc = Document()  # 创建DOM文档对象
        self.anno = self.doc.createElement('annotation')  # 创建根元素
        self.doc.appendChild(self.anno)
 
        self.add_folder()
        self.add_path()
        self.add_source()
        self.add_segmented()
 
        # self.add_filename()
        # self.add_pic_size(width_text_str=str(width), height_text_str=str(height), depth_text_str=str(depth))
 
    def add_folder(self, floder_text_str='JPEGImages'):
        floder = self.doc.createElement('floder')  ##建立自己的开头
        floder_text = self.doc.createTextNode(floder_text_str)  ##建立自己的文本信息
        floder.appendChild(floder_text)  ##自己的内容
        self.anno.appendChild(floder)
 
    def add_filename(self, filename_text_str='00000.jpg'):
        filename = self.doc.createElement('filename')
        filename_text = self.doc.createTextNode(filename_text_str)
        filename.appendChild(filename_text)
        self.anno.appendChild(filename)
 
    def add_path(self, path_text_str="None"):
        path = self.doc.createElement('path')
        path_text = self.doc.createTextNode(path_text_str)
        path.appendChild(path_text)
        self.anno.appendChild(path)
 
    def add_source(self, database_text_str="Unknow"):
        source = self.doc.createElement('source')
        database = self.doc.createElement('database')
        database_text = self.doc.createTextNode(database_text_str)  # 元素内容写入
        database.appendChild(database_text)
        source.appendChild(database)
        self.anno.appendChild(source)
 
    def add_pic_size(self, width_text_str="0", height_text_str="0", depth_text_str="3"):
        size = self.doc.createElement('size')
        width = self.doc.createElement('width')
        width_text = self.doc.createTextNode(width_text_str)  # 元素内容写入
        width.appendChild(width_text)
        size.appendChild(width)
 
        height = self.doc.createElement('height')
        height_text = self.doc.createTextNode(height_text_str)
        height.appendChild(height_text)
        size.appendChild(height)
 
        depth = self.doc.createElement('depth')
        depth_text = self.doc.createTextNode(depth_text_str)
        depth.appendChild(depth_text)
        size.appendChild(depth)
 
        self.anno.appendChild(size)
 
    def add_segmented(self, segmented_text_str="0"):
        segmented = self.doc.createElement('segmented')
        segmented_text = self.doc.createTextNode(segmented_text_str)
        segmented.appendChild(segmented_text)
        self.anno.appendChild(segmented)
 
    def add_object(self,
                   name_text_str="None",
                   xmin_text_str="0",
                   ymin_text_str="0",
                   xmax_text_str="0",
                   ymax_text_str="0",
                   pose_text_str="Unspecified",
                   truncated_text_str="0",
                   difficult_text_str="0"):
        object = self.doc.createElement('object')
        name = self.doc.createElement('name')
        name_text = self.doc.createTextNode(name_text_str)
        name.appendChild(name_text)
        object.appendChild(name)
 
        pose = self.doc.createElement('pose')
        pose_text = self.doc.createTextNode(pose_text_str)
        pose.appendChild(pose_text)
        object.appendChild(pose)
 
        truncated = self.doc.createElement('truncated')
        truncated_text = self.doc.createTextNode(truncated_text_str)
        truncated.appendChild(truncated_text)
        object.appendChild(truncated)
 
        difficult = self.doc.createElement('Difficult')
        difficult_text = self.doc.createTextNode(difficult_text_str)
        difficult.appendChild(difficult_text)
        object.appendChild(difficult)
 
        bndbox = self.doc.createElement('bndbox')
        xmin = self.doc.createElement('xmin')
        xmin_text = self.doc.createTextNode(xmin_text_str)
        xmin.appendChild(xmin_text)
        bndbox.appendChild(xmin)
 
        ymin = self.doc.createElement('ymin')
        ymin_text = self.doc.createTextNode(ymin_text_str)
        ymin.appendChild(ymin_text)
        bndbox.appendChild(ymin)
 
        xmax = self.doc.createElement('xmax')
        xmax_text = self.doc.createTextNode(xmax_text_str)
        xmax.appendChild(xmax_text)
        bndbox.appendChild(xmax)
 
        ymax = self.doc.createElement('ymax')
        ymax_text = self.doc.createTextNode(ymax_text_str)
        ymax.appendChild(ymax_text)
        bndbox.appendChild(ymax)
        object.appendChild(bndbox)
 
        self.anno.appendChild(object)
 
    def get_anno(self):
        return self.anno
 
    def get_doc(self):
        return self.doc
 
    def save_doc(self, save_path):
        with open(save_path, "w+") as f:
            self.doc.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')

def parse_txt(file_dir, file_name):
    # 读取坐标
    fr = open(os.path.join(file_dir, file_name))
    points = []
    for line in fr.readlines():  # 逐行读取，滤除空格等
        # lineArr = line.strip().split(', ')
        lineArr = line.split(' ')
        label_name = lineArr[0]
        points.append([float(lineArr[1]),float(lineArr[2]), float(lineArr[3]),float((lineArr[-1]).split("\n")[0]), int(label_name)])
    return points


def main(txt_path, xml_path, raw_image_path):
    if not os.path.exists(xml_path):
        os.makedirs(xml_path)
    path_txt = os.listdir(txt_path)
    for i in path_txt:
        name = (i.split('.'))[0]
        jpg_name = name+".jpg"
        image_path = os.path.join(raw_image_path, jpg_name)
        image_path = image_path.replace("\\", "/")
        image = cv2.imread(image_path)
        height = image.shape[0]
        width = image.shape[1]
    
        xml_anno = CreateAnno()
        xml_anno.add_filename(image_path)
        xml_anno.add_pic_size(width_text_str=str(width), height_text_str=str(height), depth_text_str=str(3))
        coordis = parse_txt(txt_path, i)
        for index in coordis:
            xml_anno.add_object(name_text_str=str(index[4]),
                                xmin_text_str=str(int(index[0])),
                                ymin_text_str=str(int(index[1])),
                                xmax_text_str=str(int(index[2])),
                                ymax_text_str=str(int(index[3])))
        save_xml_path = os.path.join(xml_path, i.replace(".txt", ".xml"))
        xml_anno.save_doc(save_xml_path)


