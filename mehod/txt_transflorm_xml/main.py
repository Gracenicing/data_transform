"""
将txt文件转成labelImg标记的xml
python main.py param1 param2 param3
param1:  txt文件所在的文件夹的路径
param2： 保存的xml文件所在的文件夹路径
param3:  原始图片的路径
例如：
命令行输入：
python main.py C:/data_convert_tool/txt_transflorm_xml/picture/txt/ C:/data_convert_tool/txt_transflorm_xml/picture/xml/ C:/data_convert_tool/txt_transflorm_xml/picture/image
"""

import sys
import os
import cv2
from create_xml_anno import CreateAnno

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


if __name__ == "__main__":
    # txt_path = sys.argv[1]
    # xml_path = sys.argv[2]
    # raw_image_path = sys.argv[3]
    txt_path = r'C:/data_convert_tool/txt_transflorm_xml/picture/txt/'
    xml_path = r'C:/data_convert_tool/txt_transflorm_xml/picture/xml/'
    raw_image_path = r'C:/data_convert_tool/txt_transflorm_xml/picture/image'
    main(txt_path, xml_path, raw_image_path)