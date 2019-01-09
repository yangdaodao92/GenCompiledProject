import glob
import os
import time

replace_dic = {}
structure_path = 'E:\\Works\\ReplaceProject'
# 遍历一个文件夹下的所有文件

index = 0
for filename in glob.glob('ReplaceProject' + '\\**\\*', recursive=True):
    if os.path.isfile(filename):
        label = os.path.basename(filename)
        local_location = filename
        remote_location = 'app_location' + filename.split('gcj_cstm_task_manager')[1].replace('\\', '/')
        replace_dic[local_location] = remote_location
        print(index)
        print(label)
        print(local_location)
        print(remote_location)
        print(os.path.split(filename))
        index += 1

# for dir_name in glob.glob('ReplaceProject/*'):
#     print(os.path.split(dir_name)[-1])
#     print(os.path.getctime(dir_name))
#     print(time.localtime(os.path.getctime(dir_name)))

# print(os.path.join('ReplaceProject', os.listdir('ReplaceProject')[0]))
# print(time.time() - os.path.getctime(os.path.join('qqq', os.listdir('qqq')[0])))
# print(os.path.getctime('D:\OtherSource\PyCharm\Glodon\GenCompiledProject'))
# print(os.path.getctime('D:\OtherSource\PyCharm\Glodon\GenCompiledProject\\test'))