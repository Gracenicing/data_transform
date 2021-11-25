# -*- coding: utf-8 -*-
from genericpath import exists
import sys
import os
root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if root_path not in sys.path:
    sys.path.append(root_path)
sys.path=[r'C:/data_convert_tool'] + sys.path
from typing import Text 
import sysconfig
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore
import json
from tqdm import tqdm
import cv2
import data_transform.json_transform_xml as jx
import data_transform.json_transform_txt as jt
import data_transform.xml_transform_json as xj
import data_transform.xml_transform_txt as xt
import data_transform.txt_transform_json as tj
import data_transform.txt_transflorm_xml as tx



class Json2Xml(QWidget):
    def __init__(self):
        super().__init__()
        
        self.title = QLabel('加载json文件路径:')
        self.author = QLabel('保存xml文件路径:')
        
        self.titleEdit_1 = QLineEdit()
        self.titleEdit_2= QLineEdit()
        self.reviewEdit = QTextEdit()

        self.btn1 = QPushButton(self)
        self.btn1.setStyleSheet("image:url(../pics/file.jpg);")
        self.btn1.clicked.connect(self.slot_btn_choose_json_Dir)
        

        self.btn2 = QPushButton(self)
        self.btn2.setStyleSheet("image:url(../pics/file.jpg);")
        self.btn2.clicked.connect(self.slot_btn_choose_xml_Dir)

        self.btn3 = QPushButton("转换", self)
        self.btn3.clicked.connect(self.slot_json_transform_xml_main)

        grid = QGridLayout()
        grid.setSpacing(10)
 
        grid.addWidget(self.title, 1, 0)
        grid.addWidget(self.titleEdit_1, 1, 1)
        grid.addWidget(self.btn1, 1, 2)
 
        grid.addWidget(self.author, 2, 0)
        grid.addWidget(self.titleEdit_2, 2, 1)
        grid.addWidget(self.btn2, 2, 2)
 
        grid.addWidget(self.btn3, 3, 0)
        grid.addWidget(self.reviewEdit, 3, 1, 5, 1)

        self.setLayout(grid)
        self.setGeometry(500, 400, 600, 600)
        self.setWindowTitle("json_transform_xml")

    def slot_btn_choose_json_Dir(self):
        dir_choose = QFileDialog.getExistingDirectory(self,  "选取文件夹")
        self.titleEdit_1.setText(str(dir_choose))

    def slot_btn_choose_xml_Dir(self):
        dir_choose = QFileDialog.getExistingDirectory(self,  "选取文件夹")
        self.titleEdit_2.setText(str(dir_choose))

    def slot_json_transform_xml_main(self):
        root_json_dir = self.titleEdit_1.text()
        root_save_xml_dir = self.titleEdit_2.text()

        # root_json_dir = r"C:\data_convert_tool\picture\label"     # json文件夹路径
        # root_save_xml_dir = r"C:\data_convert_tool\picture\xml"  # 转换后保存的xml文件夹路径
        self.reviewEdit.append("<font color=\"#0000FF\">转换开始</font> ")
        for json_filename in tqdm(os.listdir(root_json_dir)):
            json_path = os.path.join(root_json_dir, json_filename)
            save_xml_path = os.path.join(root_save_xml_dir, json_filename.replace(".json", ".xml"))
            filepath, tmpfilename = os.path.split(json_filename)
            shotname, extension = os.path.splitext(tmpfilename)
            img_path = shotname+".jpg"
            save_xml_path = save_xml_path.replace("\\", '/')
           
            jx.json_covert_xml(json_path, save_xml_path,img_path, process_mode="rectangle")
            self.reviewEdit.append(save_xml_path)
            # json_transform_xml(json_path, save_xml_path,img_path, process_mode="polygon")
            # json_transform_xml(json_path, save_xml_path, process_mode="polygon")
        self.reviewEdit.append("<font color=\"#0000FF\">转换完成！！！</font> ")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 
        
    def center(self):
        #获得窗口
        qr = self.frameGeometry()
        #获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        #显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())
class Json2Txt(QWidget):
    def __init__(self):
        super().__init__()
        
        self.title = QLabel('加载json文件路径:')
        self.author = QLabel('保存txt文件路径:')
        self.title2 = QLabel('保存class name文件路径:')
        
        self.titleEdit_1 = QLineEdit()
        self.titleEdit_2= QLineEdit()
        self.titleEdit_3 = QLineEdit()
        self.reviewEdit = QTextEdit()

        self.btn1 = QPushButton(self)
        self.btn1.setStyleSheet("image:url(../pics/file.jpg);")
        self.btn1.clicked.connect(self.slot_btn_choose_json_Dir)
        
        self.btn2 = QPushButton(self)
        self.btn2.setStyleSheet("image:url(../pics/file.jpg);")
        self.btn2.clicked.connect(self.slot_btn_choose_txt_Dir)

        self.btn3 = QPushButton(self)
        self.btn3.setStyleSheet("image:url(../pics/file.jpg);")
        self.btn3.clicked.connect(self.slot_btn_choose_save_txt_Dir)

        self.btn4 = QPushButton("转换", self)
        self.btn4.clicked.connect(self.slot_json_transform_txt_main)

        grid = QGridLayout()
        grid.setSpacing(10)
 
        grid.addWidget(self.title, 1, 0)
        grid.addWidget(self.titleEdit_1, 1, 1)
        grid.addWidget(self.btn1, 1, 2)
 
        grid.addWidget(self.author, 2, 0)
        grid.addWidget(self.titleEdit_2, 2, 1)
        grid.addWidget(self.btn2, 2, 2)
 
        grid.addWidget(self.title2, 3, 0)
        grid.addWidget(self.titleEdit_3, 3, 1)
        grid.addWidget(self.btn3, 3, 2)

        grid.addWidget(self.btn4, 4, 0)
        grid.addWidget(self.reviewEdit, 4, 1, 5, 1)

        self.setLayout(grid)
        self.setGeometry(500, 400, 600, 600)
        self.setWindowTitle("json_transform_txt")
        
    def slot_btn_choose_json_Dir(self):
        dir_choose = QFileDialog.getExistingDirectory(self,  "选取文件夹")
        self.titleEdit_1.setText(str(dir_choose))

    def slot_btn_choose_txt_Dir(self):
        dir_choose = QFileDialog.getExistingDirectory(self,  "选取文件夹")
        self.titleEdit_2.setText(str(dir_choose))

    def slot_btn_choose_save_txt_Dir(self):
        dir_choose = QFileDialog.getExistingDirectory(self,  "选取文件夹")
        self.titleEdit_3.setText(str(dir_choose))

    def slot_json_transform_txt_main(self):
        
        dir_json = self.titleEdit_1.text()
        dir_txt = self.titleEdit_2.text()
        class_txt = self.titleEdit_3.text()

        jt.get_class_index(dir_json, class_txt)

        if not os.path.exists(dir_txt):
            os.makedirs(dir_txt)

        class_txt = os.path.join(class_txt, "class_txt.txt")
        class_txt = class_txt.replace("\\", '/')
        with open(class_txt, 'r') as f:
            class_dict = f.readline()

        self.reviewEdit.append("<font color=\"#0000FF\">转换开始</font> ")
        for json_name in tqdm(os.listdir(dir_json)):
            # print('cnt=%d,name=%s'%(cnt,json_name))
            path_json = os.path.join(dir_json, json_name)
            path_json = path_json.replace("\\", '/')
            path_txt = os.path.join(dir_txt, json_name.replace('.json','.txt'))
            path_txt = path_txt.replace("\\", '/')
            jt.json_convert_txt(path_json, path_txt, class_dict)
            self.reviewEdit.append(path_txt)
        self.reviewEdit.append("<font color=\"#0000FF\">转换完成！！！</font> ")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 
class Xml2Json(QWidget):
    def __init__(self):
        super().__init__()
        
        self.title_1 = QLabel('加载xml文件路径:')
        self.title_2 = QLabel('保存json文件路径:')
        self.title_3= QLabel('image文件夹路径:')
        
        self.titleEdit_1 = QLineEdit()
        self.titleEdit_2 = QLineEdit()
        self.titleEdit_3 = QLineEdit()
        self.reviewEdit = QTextEdit()

        self.btn1 = QPushButton(self)
        self.btn1.setStyleSheet("image:url(../pics/file.jpg);")
        self.btn1.clicked.connect(self.slot_btn_choose_xml_Dir)
        

        self.btn2 = QPushButton(self)
        self.btn2.setStyleSheet("image:url(../pics/file.jpg);")
        self.btn2.clicked.connect(self.slot_btn_choose_json_Dir)

        self.btn3 = QPushButton(self)
        self.btn3.setStyleSheet("image:url(../pics/file.jpg);")
        self.btn3.clicked.connect(self.slot_btn_choose_image_Dir)

        self.btn4 = QPushButton("转换", self)
        self.btn4.clicked.connect(self.slot_xml_transform_json_main)

        grid = QGridLayout()
        grid.setSpacing(10)
 
        grid.addWidget(self.title_1, 1, 0)
        grid.addWidget(self.titleEdit_1, 1, 1)
        grid.addWidget(self.btn1, 1, 2)
 
        grid.addWidget(self.title_2, 2, 0)
        grid.addWidget(self.titleEdit_2, 2, 1)
        grid.addWidget(self.btn2, 2, 2)

        grid.addWidget(self.title_3, 3, 0)
        grid.addWidget(self.titleEdit_3, 3, 1)
        grid.addWidget(self.btn3, 3, 2)
 
        grid.addWidget(self.btn4, 4, 0)
        grid.addWidget(self.reviewEdit, 4, 1, 5, 1)

        self.setLayout(grid)
        self.setGeometry(500, 400, 600, 600)
        self.setWindowTitle("xml_transform_json")

    def slot_btn_choose_xml_Dir(self):
        dir_choose = QFileDialog.getExistingDirectory(self,  "选取文件夹")
        self.titleEdit_1.setText(str(dir_choose))

    def slot_btn_choose_json_Dir(self):
        dir_choose = QFileDialog.getExistingDirectory(self,  "选取文件夹")
        self.titleEdit_2.setText(str(dir_choose))

    def slot_btn_choose_image_Dir(self):
        dir_choose = QFileDialog.getExistingDirectory(self,  "选取文件夹")
        self.titleEdit_3.setText(str(dir_choose))

    def slot_xml_transform_json_main(self):
        xml_path = self.titleEdit_1.text()
        json_path = self.titleEdit_2.text()
        raw_image_path = self.titleEdit_3.text()

        xml_path = xml_path.replace("\\", "/")
        json_path = json_path.replace("\\", "/")
        raw_image_path = raw_image_path.replace("\\", "/")
        path_xml = os.listdir(xml_path)
        self.reviewEdit.append("<font color=\"#0000FF\">转换开始</font> ")
        for file_name in path_xml:
            str_json = xj.generate_json(xml_path, file_name, raw_image_path)
            json_data = json.dumps(str_json)
            jsonfile_name = file_name.replace(".xml",".json")
            path = os.path.join(json_path, jsonfile_name)
            path = path.replace("\\", "/")
            f = open(path, 'w')
            f.write(json_data)
            f.close()
            self.reviewEdit.append(path)
            
        self.reviewEdit.append("<font color=\"#0000FF\">转换完成！！！</font> ")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 
        
    def center(self):
        #获得窗口
        qr = self.frameGeometry()
        #获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        #显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())
class Xml2Txt(QWidget):
    def __init__(self):
        super().__init__()
        
        self.title = QLabel('加载xml文件路径:')
        self.author = QLabel('保存txt文件路径:')
        self.title2 = QLabel('保存class name文件路径:')
        
        self.titleEdit_1 = QLineEdit()
        self.titleEdit_2= QLineEdit()
        self.titleEdit_3 = QLineEdit()
        self.reviewEdit = QTextEdit()

        self.btn1 = QPushButton(self)
        self.btn1.setStyleSheet("image:url(../pics/file.jpg);")
        self.btn1.clicked.connect(self.slot_btn_choose_json_Dir)
        
        self.btn2 = QPushButton(self)
        self.btn2.setStyleSheet("image:url(../pics/file.jpg);")
        self.btn2.clicked.connect(self.slot_btn_choose_txt_Dir)

        self.btn3 = QPushButton(self)
        self.btn3.setStyleSheet("image:url(../pics/file.jpg);")
        self.btn3.clicked.connect(self.slot_btn_choose_save_txt_Dir)

        self.btn4 = QPushButton("转换", self)
        self.btn4.clicked.connect(self.slot_xml_transform_txt_main)

        grid = QGridLayout()
        grid.setSpacing(10)
 
        grid.addWidget(self.title, 1, 0)
        grid.addWidget(self.titleEdit_1, 1, 1)
        grid.addWidget(self.btn1, 1, 2)
 
        grid.addWidget(self.author, 2, 0)
        grid.addWidget(self.titleEdit_2, 2, 1)
        grid.addWidget(self.btn2, 2, 2)
 
        grid.addWidget(self.title2, 3, 0)
        grid.addWidget(self.titleEdit_3, 3, 1)
        grid.addWidget(self.btn3, 3, 2)

        grid.addWidget(self.btn4, 4, 0)
        grid.addWidget(self.reviewEdit, 4, 1, 5, 1)

        self.setLayout(grid)
        self.setGeometry(500, 400, 600, 600)
        self.setWindowTitle("xml_transform_txt")
        
    def slot_btn_choose_json_Dir(self):
        dir_choose = QFileDialog.getExistingDirectory(self,  "选取文件夹")
        self.titleEdit_1.setText(str(dir_choose))

    def slot_btn_choose_txt_Dir(self):
        dir_choose = QFileDialog.getExistingDirectory(self,  "选取文件夹")
        self.titleEdit_2.setText(str(dir_choose))

    def slot_btn_choose_save_txt_Dir(self):
        dir_choose = QFileDialog.getExistingDirectory(self,  "选取文件夹")
        self.titleEdit_3.setText(str(dir_choose))

    def slot_xml_transform_txt_main(self):
        
        xml_path = self.titleEdit_1.text()
        dir_txt = self.titleEdit_2.text()
        class_txt = self.titleEdit_3.text()

        xt.get_class_index(xml_path, class_txt)

        if not os.path.exists(dir_txt):
            os.makedirs(dir_txt)

        class_txt = os.path.join(class_txt, "class_txt.txt")
        class_txt = class_txt.replace("\\", '/')
        with open(class_txt, 'r') as f:
            class_dict = f.readline()

        self.reviewEdit.append("<font color=\"#0000FF\">转换开始</font> ")
        
        for json_name in tqdm(os.listdir(xml_path)):
            path_xml = os.path.join(xml_path, json_name)
            path_txt = os.path.join(dir_txt, json_name.replace('.xml','.txt'))
            path_txt = path_txt.replace("\\", "/")
            with open(path_txt, "w+") as f:
                points = xt.parse_xml(path_xml)
                for one_rect in points:
                    class_dict = eval(str(class_dict))
                    label_index = str(class_dict[str(one_rect[4])])
                    f.writelines( label_index + " " + str(one_rect[0]) + " " + str(one_rect[1]) + " "+ str(one_rect[2]) + " " + str(one_rect[3])+"\n")
            self.reviewEdit.append(path_txt)
        self.reviewEdit.append("<font color=\"#0000FF\">转换完成！！！</font> ")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 
class Txt2Json(QWidget):
    def __init__(self):
        super().__init__()
        
        self.title_1 = QLabel('加载txt文件路径:')
        self.title_2 = QLabel('保存json文件路径:')
        self.title_3= QLabel('image文件夹路径:')
        
        self.titleEdit_1 = QLineEdit()
        self.titleEdit_2 = QLineEdit()
        self.titleEdit_3 = QLineEdit()
        self.reviewEdit = QTextEdit()

        self.btn1 = QPushButton(self)
        self.btn1.setStyleSheet("image:url(../pics/file.jpg);")
        self.btn1.clicked.connect(self.slot_btn_choose_xml_Dir)
        

        self.btn2 = QPushButton(self)
        self.btn2.setStyleSheet("image:url(../pics/file.jpg);")
        self.btn2.clicked.connect(self.slot_btn_choose_json_Dir)

        self.btn3 = QPushButton(self)
        self.btn3.setStyleSheet("image:url(../pics/file.jpg);")
        self.btn3.clicked.connect(self.slot_btn_choose_image_Dir)

        self.btn4 = QPushButton("转换", self)
        self.btn4.clicked.connect(self.slot_txt_transform_json_main)

        grid = QGridLayout()
        grid.setSpacing(10)
 
        grid.addWidget(self.title_1, 1, 0)
        grid.addWidget(self.titleEdit_1, 1, 1)
        grid.addWidget(self.btn1, 1, 2)
 
        grid.addWidget(self.title_2, 2, 0)
        grid.addWidget(self.titleEdit_2, 2, 1)
        grid.addWidget(self.btn2, 2, 2)

        grid.addWidget(self.title_3, 3, 0)
        grid.addWidget(self.titleEdit_3, 3, 1)
        grid.addWidget(self.btn3, 3, 2)
 
        grid.addWidget(self.btn4, 4, 0)
        grid.addWidget(self.reviewEdit, 4, 1, 5, 1)

        self.setLayout(grid)
        self.setGeometry(500, 400, 600, 600)
        self.setWindowTitle("txt_transform_json")

    def slot_btn_choose_xml_Dir(self):
        dir_choose = QFileDialog.getExistingDirectory(self,  "选取文件夹")
        self.titleEdit_1.setText(str(dir_choose))

    def slot_btn_choose_json_Dir(self):
        dir_choose = QFileDialog.getExistingDirectory(self,  "选取文件夹")
        self.titleEdit_2.setText(str(dir_choose))

    def slot_btn_choose_image_Dir(self):
        dir_choose = QFileDialog.getExistingDirectory(self,  "选取文件夹")
        self.titleEdit_3.setText(str(dir_choose))

    def slot_txt_transform_json_main(self):
        txt_path = self.titleEdit_1.text()
        json_path = self.titleEdit_2.text()
        raw_image_path = self.titleEdit_3.text()

        txt_path = txt_path.replace("\\", "/")
        json_path = json_path.replace("\\", "/")
        raw_image_path = raw_image_path.replace("\\", "/")
        self.reviewEdit.append("<font color=\"#0000FF\">转换开始</font> ")
        file_name_list = [file_name for file_name in os.listdir(txt_path) \
                            if file_name.lower().endswith('txt')]
        for file_name in file_name_list:

            str_json = tj.generate_json(txt_path, file_name, raw_image_path)
            json_data = json.dumps(str_json)
            jsonfile_name = file_name.replace(".txt",".json")
            path = os.path.join(json_path, jsonfile_name)
            path = path.replace("\\", "/")
            f = open(path, 'w')
            f.write(json_data)
            f.close()
            self.reviewEdit.append(path)
            
        self.reviewEdit.append("<font color=\"#0000FF\">转换完成！！！</font> ")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 
        
    def center(self):
        #获得窗口
        qr = self.frameGeometry()
        #获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        #显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())
class Txt2Xml(QWidget):
    def __init__(self):
        super().__init__()
        
        self.title_1 = QLabel('加载txt文件路径:')
        self.title_2 = QLabel('保存xml文件路径:')
        self.title_3= QLabel('image文件夹路径:')
        
        self.titleEdit_1 = QLineEdit()
        self.titleEdit_2 = QLineEdit()
        self.titleEdit_3 = QLineEdit()
        self.reviewEdit = QTextEdit()

        self.btn1 = QPushButton(self)
        self.btn1.setStyleSheet("image:url(../pics/file.jpg);")
        self.btn1.clicked.connect(self.slot_btn_choose_xml_Dir)
        

        self.btn2 = QPushButton(self)
        self.btn2.setStyleSheet("image:url(../pics/file.jpg);")
        self.btn2.clicked.connect(self.slot_btn_choose_json_Dir)

        self.btn3 = QPushButton(self)
        self.btn3.setStyleSheet("image:url(../pics/file.jpg);")
        self.btn3.clicked.connect(self.slot_btn_choose_image_Dir)

        self.btn4 = QPushButton("转换", self)
        self.btn4.clicked.connect(self.slot_txt_transform_xml_main)

        grid = QGridLayout()
        grid.setSpacing(10)
 
        grid.addWidget(self.title_1, 1, 0)
        grid.addWidget(self.titleEdit_1, 1, 1)
        grid.addWidget(self.btn1, 1, 2)
 
        grid.addWidget(self.title_2, 2, 0)
        grid.addWidget(self.titleEdit_2, 2, 1)
        grid.addWidget(self.btn2, 2, 2)

        grid.addWidget(self.title_3, 3, 0)
        grid.addWidget(self.titleEdit_3, 3, 1)
        grid.addWidget(self.btn3, 3, 2)
 
        grid.addWidget(self.btn4, 4, 0)
        grid.addWidget(self.reviewEdit, 4, 1, 5, 1)

        self.setLayout(grid)
        self.setGeometry(500, 400, 600, 600)
        self.setWindowTitle("txt_transform_xml")

    def slot_btn_choose_xml_Dir(self):
        dir_choose = QFileDialog.getExistingDirectory(self,  "选取文件夹")
        self.titleEdit_1.setText(str(dir_choose))

    def slot_btn_choose_json_Dir(self):
        dir_choose = QFileDialog.getExistingDirectory(self,  "选取文件夹")
        self.titleEdit_2.setText(str(dir_choose))

    def slot_btn_choose_image_Dir(self):
        dir_choose = QFileDialog.getExistingDirectory(self,  "选取文件夹")
        self.titleEdit_3.setText(str(dir_choose))

    def slot_txt_transform_xml_main(self):
        txt_path = self.titleEdit_1.text()
        xml_path = self.titleEdit_2.text()
        raw_image_path = self.titleEdit_3.text()

        txt_path = txt_path.replace("\\", "/")
        xml_path = xml_path.replace("\\", "/")
        raw_image_path = raw_image_path.replace("\\", "/")
        self.reviewEdit.append("<font color=\"#0000FF\">转换开始</font> ") 
        for i in tqdm(os.listdir(txt_path)):
            if exists(os.path.join(raw_image_path, i.replace('.txt', '.jpg'))):
                image_path = os.path.join(raw_image_path, i.replace('.txt', '.jpg'))
                image_path = image_path.replace("\\", "/")
                image = cv2.imread(image_path)
                height = image.shape[0]
                width = image.shape[1]
            
                xml_anno = tx.CreateAnno()
                xml_anno.add_filename(image_path)
                xml_anno.add_pic_size(width_text_str=str(width), height_text_str=str(height), depth_text_str=str(3))
                coordis = tx.parse_txt(txt_path, i)
                for index in coordis:
                    xml_anno.add_object(name_text_str=str(index[0]),
                                xmin_text_str= index[1],
                                ymin_text_str= index[2],
                                xmax_text_str= index[3],
                                ymax_text_str= index[4])
                save_xml_path = os.path.join(xml_path, i.replace(".txt", ".xml"))
                save_xml_path = save_xml_path.replace("\\", "/")
                xml_anno.save_doc(save_xml_path)
                self.reviewEdit.append(save_xml_path)
            
            elif exists(os.path.join(raw_image_path, i.replace('.txt', '.bmp'))):
                image_path = os.path.join(raw_image_path, i.replace('.txt', '.bmp'))
                image_path = image_path.replace("\\", "/")
                image = cv2.imread(image_path)
                height = image.shape[0]
                width = image.shape[1]
            
                xml_anno = tx.CreateAnno()
                xml_anno.add_filename(image_path)
                xml_anno.add_pic_size(width_text_str=str(width), height_text_str=str(height), depth_text_str=str(3))
                coordis = tx.parse_txt(txt_path, i)
                for index in coordis:
                    xml_anno.add_object(name_text_str=str(index[0]),
                                xmin_text_str= str(int(index[1])),
                                ymin_text_str= str(int(index[2])),
                                xmax_text_str= str(int(index[3])),
                                ymax_text_str= str(int(index[4])))
                save_xml_path = os.path.join(xml_path, i.replace(".txt", ".xml"))
                save_xml_path = save_xml_path.replace("\\", "/")
                xml_anno.save_doc(save_xml_path)
                self.reviewEdit.append(save_xml_path)
        self.reviewEdit.append("<font color=\"#0000FF\">转换完成！！！</font> ")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 
        
    def center(self):
        #获得窗口
        qr = self.frameGeometry()
        #获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        #显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
# 主窗口
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.json_transform_xml_btn = QPushButton("json_transform_xml", self)
        self.json_transform_xml_btn.resize(130, 30)
        self.json_transform_xml_btn.move(50, 50)

        self.json_transform_txt_btn = QPushButton("json_transform_txt", self)
        self.json_transform_txt_btn.resize(130, 30)
        self.json_transform_txt_btn.move(50, 100)

        self.xml_transform_json_btn = QPushButton("xml_transform_json", self)
        self.xml_transform_json_btn.resize(130, 30)
        self.xml_transform_json_btn.move(50, 150)

        self.xml_transform_txt_btn = QPushButton("xml_transform_txt", self)
        self.xml_transform_txt_btn.resize(130, 30)
        self.xml_transform_txt_btn.move(50, 200)

        self.txt_transform_json_btn = QPushButton("txt_transform_json", self)
        self.txt_transform_json_btn.resize(130, 30)
        self.txt_transform_json_btn.move(50, 250)

        self.txt_transform_xml_btn = QPushButton("txt_transform_xml", self)
        self.txt_transform_xml_btn.resize(130, 30)
        self.txt_transform_xml_btn.move(50, 300)


        self.setGeometry(100, 100, 500, 500)
        self.setWindowIcon(QIcon('../pics/1.jpg'))
        self.setWindowTitle('DataFormatTransform')
        self.show()

    def center(self):
        #获得窗口
        qr = self.frameGeometry()
        #获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        #显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

# 启动整个项目
def main():
    app = QApplication(sys.argv)
    main_interface = MyWindow()
    main_interface.show()

    showJson2xml = Json2Xml()
    main_interface.json_transform_xml_btn.clicked.connect(showJson2xml.show)

    showJson2Txt = Json2Txt()
    main_interface.json_transform_txt_btn.clicked.connect(showJson2Txt.show)

    showXml2Json = Xml2Json()
    main_interface.xml_transform_json_btn.clicked.connect(showXml2Json.show)

    showXml2Txt = Xml2Txt()
    main_interface.xml_transform_txt_btn.clicked.connect(showXml2Txt.show)

    showTxt2Json = Txt2Json()
    main_interface.txt_transform_json_btn.clicked.connect(showTxt2Json.show)

    showTxt2Xml = Txt2Xml()
    main_interface.txt_transform_xml_btn.clicked.connect(showTxt2Xml.show)

    sys.exit(app.exec_())

if __name__=="__main__":
    main()