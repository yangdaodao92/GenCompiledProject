import yaml
import os
import shutil
import glob

# 测试yaml
# local_project = {
#     'task': {
#         'src_location': 'D:\IdeaSource\Glodon\java\gcj_cstm_task_manager',
#         'des_location': 'E:\Works\Publication Directory\gcj_cstm_task_manager'
#     }
# }
#
# print(yaml.dump(local_project, default_flow_style=False))
#
# file = open('conf.yaml', 'w')
# file.write(yaml.dump(local_project, default_flow_style=False))
# file.flush()
#
# print(yaml.load(file))
# conf = yaml.load(file)


# 测试创建文件夹
# directory = 'E:\\Works\\structure'
# if not os.path.exists(directory):
#     os.makedirs(directory)

# shutil.rmtree(directory)

# 遍历一个文件夹下的所有文件
for filename in glob.glob('E:\\Works\\Publication Directory\\gcj_cstm_task_manager\\**\\*', recursive=True):
    print(filename)


# 模拟一次
# file = open('conf.yaml', 'r')
# local_project_config = yaml.load(file)
#
# source_files = [
#     'D:\IdeaSource\Glodon\java\gcj_cstm_task_manager\src\main\java\com\gcj\service\cs\CustomerService.java',
#     'D:\IdeaSource\Glodon\java\gcj_cstm_task_manager\src\main\\resources\mybatis-mapper\member\OnlinePurchaseOrderMapper.xml',
#     'D:\IdeaSource\Glodon\java\gcj_cstm_task_manager\src\main\webapp\javascripts\job\job-list.js'
# ]
#
# target_files = {}
# for source_file in source_files:
#     for (name, obj) in local_project_config.items():
#         _file = source_file.split('\\src\\main\\')
#         if _file[0] == obj['source_location']:
#             compiled_location_head = '\\'.join(str(obj['compiled_location']).split('\\')[:-1])
#             if _file[1].startswith('java'):
#                 target_files[obj['compiled_location'] + '\\WEB-INF\\classes\\'
#                              + _file[1].replace('java\\', '').replace('.java', '.class')] = compiled_location_head
#             if _file[1].startswith('resource'):
#                 target_files[obj['compiled_location'] + '\\WEB-INF\\classes\\' + _file[1].replace('resources\\', '')] = compiled_location_head
#             if _file[1].startswith('webapp'):
#                 target_files[obj['compiled_location'] + '\\' + _file[1].replace('webapp\\', '')] = compiled_location_head
#
# structure_path = 'E:\\Works\\ReplaceProject'
# if os.path.exists(structure_path):
#     shutil.rmtree(structure_path)
# for (compiled_file, compiled_location_head) in target_files.items():
#     des_file_name = str(compiled_file).replace(compiled_location_head, structure_path)
#     directory = os.path.dirname(des_file_name)
#     if not os.path.exists(directory):
#         os.makedirs(directory)
#     shutil.copy(compiled_file, des_file_name)





