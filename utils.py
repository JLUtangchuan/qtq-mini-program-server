#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2022/06/29 12:24:11
@Author  :   Tang Chuan 
@Contact :   tangchuan20@mails.jlu.edu.cn
@Desc    :   一些工具函数
'''
import base64
import os
import random
import time
from io import BytesIO

import numpy as np
from PIL import Image


def img_to_base64(img_path):
    '''
    将本地图片转换为base64格式
    '''
    with open(img_path, 'rb') as f:
        img_base64 = base64.b64encode(f.read()).decode('ascii')
    return img_base64

def base64_to_img(img_base64, img_path):
    '''
    将base64格式的图片转换为本地图片
    '''
    bytes_data = base64.b64decode(img_base64)
    image = Image.open(BytesIO(bytes_data))
    # save
    image.save(img_path)
    return img_path

def get_random_file(path='static/images'):
    """
        获取随机图片
    """
    import os
    files = os.listdir(path)
    
    return os.path.join(path, random.choice(files))

def save_image(image, info="", path="static/data"):
    filename = info + str(time.time())
    filename = str(base64.urlsafe_b64encode(filename.encode("utf-8")), "utf-8") + ".jpg"
    # save image
    image_path = os.path.join(path, filename)
    image.save(image_path)
    return filename

def load_db_data(year_pth):
    """
    加载数据
    由于出处属性202302月有更新，需要对应一下
    出处、出土地、现藏地都需要更新
    """
    
    # 建立 image_path: chuchu对应字典
    image_path = np.load("static/bronze_ware_data/npy/dim_path.npy")  # 下面图片对应的文件路径
    change_dict = {
        "chuchu": np.load("static/bronze_ware_data/npy/dim_chuchu.npy"),  # 出处
        "chutudi": np.load("static/bronze_ware_data/npy/dim_birth.npy"),  # 出土地
        "xiancangdi": np.load("static/bronze_ware_data/npy/dim_where.npy"),  # 现藏地
    }
    # ware_chuchu = np.load("static/bronze_ware_data/npy/dim_chuchu.npy")  # 出处
    # newchuchu_dic = dict(zip(image_path, ware_chuchu))
    new_dic = dict(zip(image_path, zip(change_dict["chuchu"], change_dict["chutudi"], change_dict["xiancangdi"])))
    
    # 加载year_pth中的所有数据
    dic = {}
    for i,v in year_pth.items():
        dic[i] = np.load(v)
    
    # 修改出处属性
    for k, v in dic.items():
        for i in range(v.shape[0]):
            v[i][6] = new_dic[v[i][0]][0] # 出处
            v[i][5] = new_dic[v[i][0]][1] # 出土地
            v[i][4] = new_dic[v[i][0]][2] # 现藏地
            
    # 返回字典
    return dic
    

if __name__ == '__main__':
    # img_base64 = img_to_base64('./static/images/0.jpeg')
    # # print(img_base64)
    # path = base64_to_img(img_base64, './static/images/new.jpeg')
    # print(path)
    im = Image.open('./static/images/0.jpeg')
    res = save_image(im)
    print(res)


