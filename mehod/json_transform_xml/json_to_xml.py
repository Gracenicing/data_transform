"""
将labelme 标记的json文件 转成labelImg 标记的xml文件
python main.py param1 param2
param1 : json文件所在的文件夹的路径
param2： 保存的xml文件所在的文件夹路径
例如：
命令行输入：
python json_to_xml.py C:/data_convert_tool/picture/label C:/data_convert_tool/picture/xml

"""

import os
import sys
root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if root_path not in sys.path:
    sys.path.append(root_path)
sys.path=[r'C:/data_convert_tool'] + sys.path
from tqdm import tqdm
from json_transform_xml.read_json_anno import ReadAnno
from json_transform_xml.create_xml_anno import CreateAnno


def json_covert_xml(json_path, xml_path,imagePath, process_mode="rectangle"):
    json_anno = ReadAnno(json_path, process_mode=process_mode)
    width, height = json_anno.get_width_height()
    filename = json_anno.get_filename()
    coordis = json_anno.get_coordis()
 
    xml_anno = CreateAnno()
    xml_anno.add_filename(imagePath)
    xml_anno.add_pic_size(width_text_str=str(width), height_text_str=str(height), depth_text_str=str(3))
    for xmin,ymin,xmax,ymax,label in coordis:
        if((xmax-xmin)<(width*2/3)): #! ###########################################
            # xml_anno.add_object(name_text_str=str("text"),
            xml_anno.add_object(name_text_str=str(label),
                                xmin_text_str=str(int(xmin)),
                                ymin_text_str=str(int(ymin)),
                                xmax_text_str=str(int(xmax)),
                                ymax_text_str=str(int(ymax)))
 
    xml_anno.save_doc(xml_path)

def main(root_json_dir, root_save_xml_dir):
    # root_json_dir = r"C:\data_convert_tool\picture\label"     # json文件夹路径
    # root_save_xml_dir = r"C:\data_convert_tool\picture\xml"  # 转换后保存的xml文件夹路径

    for json_filename in tqdm(os.listdir(root_json_dir)):
        json_path = os.path.join(root_json_dir, json_filename)
        save_xml_path = os.path.join(root_save_xml_dir, json_filename.replace(".json", ".xml"))
        filepath, tmpfilename = os.path.split(json_filename)
        shotname, extension = os.path.splitext(tmpfilename)
        img_path = shotname+".jpg"
        json_covert_xml(json_path, save_xml_path,img_path, process_mode="rectangle")
        # jx = Json2Xml()
        # jx.reviewEdit.setText(save_xml_path)
        # json_transform_xml(json_path, save_xml_path,img_path, process_mode="polygon")
        # json_transform_xml(json_path, save_xml_path, process_mode="polygon")
    
# if __name__ == "__main__":
#     json_path = sys.argv[1]
#     xml_path = sys.argv[2]
#     main(json_path, xml_path)