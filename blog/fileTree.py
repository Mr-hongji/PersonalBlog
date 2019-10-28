import os, json
from django.http import HttpResponse
from PersonalBlog import settings


def list_dir(file_dir, type):
    '''
        通过 listdir 得到的是仅当前路径下的文件名，不包括子目录中的文件，如果需要得到所有文件需要递归
    '''

    #print ("current dir : {0}".format(file_dir))
    dir_list = os.listdir(file_dir)
    ret = [];
    for cur_file in dir_list:
        if cur_file.find('.') != 0:
            # 获取文件的绝对路径
            path = os.path.join(file_dir, cur_file)
            # 判断是否是文件还是目录需要用绝对路径
            #如果是文件
            if os.path.isfile(path):
                addNode = True
                #如果是视频页面，判断文件后缀名是不是视频格式
                if type == 'video':
                    temp_arr = cur_file.split('.')

                    if temp_arr and temp_arr[len(temp_arr) - 1:][0] in ['mp4', 'flv', 'avi', 'rmvb', 'mkv', 'swf', 'wrf', 'mov', 'smv', 'wmv']:
                        addNode = True
                    else:
                        addNode = False

                #print("{0} : is file!".format(cur_file))
                if addNode:
                    ret.append({'name': cur_file, 'isParent': False, 'path':path})
            print(path)

            #如果是目录
            #过滤名字以__开头的文件夹，因为python中会有 __pycache__ 这种缓存文件目录
            if os.path.isdir(path) and cur_file.find('__') != 0:
                #print ("{0} : is dir!".format(cur_file))
                #list_dir(path) # 递归子目录
                ret.append({'name':cur_file, 'isParent': True, 'path':path})

    return (json.dumps(ret))

import chardet
def readFile(path):
    ret = {'status':None, 'data':None, 'path':path}
    if path:
        try:
            with open(path, 'rb') as f:
                data = f.read();
                if data:
                    encoding_format = chardet.detect(data).get("encoding")  # 获取文件的编码格式
                    data = data.decode(encoding_format)
                else:
                    data = ""

                #print(data)
                ret['status'] = 1
                ret['data'] = data
        except:
            ret['status'] = 0
            ret['data'] = '文件读取失败'

    else:
        ret['status'] = 0
        ret['data'] = '文件路径错误'

    return json.dumps(ret)



# if __name__ == '__main__':
# 	list_dir('D:\pycode\PersonalBlog')