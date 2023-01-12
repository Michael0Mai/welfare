import random
import os
import datetime, time
from pathlib import Path

from django.conf import settings

# def save_img(image, dest_father_dir): # 接收并保存图片
#     # 防重名
#     p = Path(image.name)
#     img_pure_name = p.stem + '_' + str(int(time.time())) # p.stem：提取无后缀的文件名
#     img_extend_name = p.suffix # 提取后缀名
#     img_name = img_pure_name + img_extend_name # 新的文件名

#     # 创建存储路径
#     img_dir1 = os.path.join(settings.MEDIA_ROOT, dest_father_dir) # 想要保存的文件夹 
#     if not os.path.exists(img_dir1):
#         os.mkdir(img_dir1)
#     img_dir2 = os.path.join(img_dir1, datetime.datetime.now().strftime("%Y")) # 按年保存的文件夹
#     if not os.path.exists(img_dir2):
#         os.mkdir(img_dir2)
#     img_file = os.path.join(img_dir2, datetime.datetime.now().strftime("%m")) # 按月保存的文件夹
#     if not os.path.exists(img_file):
#         os.mkdir(img_file)

#     # 存储图片
#     destination = open(os.path.join(img_file, img_name), 'wb+')
#     for chunk in image.chunks(): # 对图片切片
#         destination.write(chunk) # 把切片写入
#     destination.close()

#     return img_name

# # 获取图片存储地址
# def get_img_url(request, img_file, img_name):
#     if request.is_secure():
#         protocol = 'https'
#     else:
#         protocol = 'http'
    
#     backend_relative_path = img_file + '/' + datetime.datetime.now().strftime("%Y") + '/' + datetime.datetime.now().strftime("%m") + '/' + img_name # 传回给后端ImageField要存储的图片路径
#     relative_path = settings.MEDIA_URL + backend_relative_path 
#     frontend_url = protocol + '://'+ str(request.META['HTTP_HOST']) + relative_path # 前端显示需要的图片路径
#     return {"url": frontend_url, "backend_path": backend_relative_path}

# def get_img_backend_relative_path(img_file, img_name):
#     backend_relative_path = img_file + '/' + datetime.datetime.now().strftime("%Y") + '/' + datetime.datetime.now().strftime("%m") + '/' + img_name # 传回给后端ImageField要存储的图片路径
#     return backend_relative_path

def img_proccess_save(image, file):
    # 防重名
    name = Path(image.name)
    img_pure_name = name.stem + '_' + str(int(time.time())) # p.stem：提取无后缀的文件名
    img_extend_name = name.suffix # 提取后缀名
    img_name = img_pure_name + img_extend_name # 新的文件名

    # 创建存储路径
    img_dir = os.path.join(settings.MEDIA_ROOT, file) # 想要保存的文件夹 
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
    img_file_year = os.path.join(img_dir, datetime.datetime.now().strftime("%Y")) # 按年保存的文件夹
    if not os.path.exists(img_file_year):
        os.mkdir(img_file_year)
    img_file_month = os.path.join(img_file_year, datetime.datetime.now().strftime("%m")) # 按月保存的文件夹
    if not os.path.exists(img_file_month):
        os.mkdir(img_file_month)

    # 存储图片
    destination = open(os.path.join(img_file_month, img_name), 'wb+')
    for chunk in image.chunks(): # 对图片切片
        destination.write(chunk) # 把切片写入
    destination.close()

    # 传回给后端ImageField要存储的图片路径
    backend_relative_path = file + '/' + datetime.datetime.now().strftime("%Y") + '/' + datetime.datetime.now().strftime("%m") + '/' + img_name 

    return img_name, backend_relative_path
