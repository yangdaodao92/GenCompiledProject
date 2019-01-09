# -*- coding: utf-8 -*-

import wx
import wx.xrc
import yaml
import os
import shutil
import math
import datetime
import getpass
import pyautogui
import time
from wx.lib.pubsub import pub
import threading, time
import zipfile
import glob
import wx

size = 30
structure_path = 'E:\\Works\\ReplaceProject'
jar_extract_path = structure_path + '\\' + 'jar-extract'

extract = {
    "waterdrop_admin_online": ['template.helper-', 'parser.engine-', 'waterdrop-common-'],
    "gcj_dws_hw_online": ['template.helper-', 'parser.engine-', 'waterdrop-common-']
}


# 解压文件
def un_zip(file_name, dir_path):
    zip_file = zipfile.ZipFile(file_name)
    if not dir_path:
        dir_path = os.path.splitext(file_name)[0]
    else:
        dir_path = dir_path + '\\' + os.path.splitext(file_name)[0].split('\\')[-1]
    if os.path.isdir(dir_path):
        pass
    else:
        os.makedirs(dir_path)
    for names in zip_file.namelist():
        zip_file.extract(names, dir_path)
    zip_file.close()
    return dir_path


# 拷贝文件到文件夹
def copy_file(src, dst):
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    shutil.copy(src, dst)

# 创建工作目录
if not os.path.exists(structure_path):
    os.mkdir(structure_path)


# 替换文件的窗口
class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title='文件替换工具', pos=wx.DefaultPosition,
                          size=wx.Size(1000, 900), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.project_name = None
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(223, 223, 223))
        self.SetSize(wx.Size(1000, int(math.ceil(size / 2))*45))
        replaceBsWrapper = wx.BoxSizer(wx.VERTICAL)

        # 顶部的选择按钮
        self.project_btns = wx.BoxSizer(wx.HORIZONTAL)
        self.project_btns.SetMinSize(wx.Size(-1, 20))

        self.st_project = wx.StaticText(self, wx.ID_ANY, '', wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_project.Wrap(-1)
        self.st_project.SetMinSize(wx.Size(40, -1))
        self.project_btns.Add(self.st_project, 0, wx.ALL, 5)

        self.create_project_btn('gccce', self.choose_project, 1001)
        self.create_project_btn('task', self.choose_project, 1002)
        self.create_project_btn('bg', self.choose_project, 1003)
        self.create_project_btn('api', self.choose_project, 1004)
        self.create_project_btn('master', self.choose_project, 1005)
        self.create_project_btn('dws-hw', self.choose_project, 1006)
        self.create_project_btn('dws-yz', self.choose_project, 1007)
        self.create_project_btn('water-backend', self.choose_project, 1008)
        self.create_project_btn('bid-data-interface', self.choose_project, 1009)

        replaceBsWrapper.Add(self.project_btns, 1, wx.EXPAND, 5)

        self.replaceFilePaths = []
        for i in range(int(math.ceil(size / 2))):
            gSizer = wx.GridSizer(1, 2, 0, 0)
            replaceBsI = wx.BoxSizer(wx.HORIZONTAL)
            replaceBsI.SetMinSize(wx.Size(-1, 20))
            # 标题
            replaceLabelI = wx.StaticText(self, wx.ID_ANY, str(i*2 + 1), wx.DefaultPosition, wx.DefaultSize, 0)
            replaceBsI.Add(replaceLabelI, 0, wx.ALL, 5)
            # TextCtrl
            replaceFilePathI = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(1000, -1), 0)
            replaceFilePathI.Bind(wx.EVT_KEY_DOWN, self.TextCtrlEnterDown)
            self.replaceFilePaths.append(replaceFilePathI)

            replaceBsI.Add(replaceFilePathI, 0, wx.ALL, 5)
            gSizer.Add(replaceBsI, 1, wx.EXPAND, 5)
            # 渲染第二列
            if i*2 + 2 <= size:
                replaceBsI2 = wx.BoxSizer(wx.HORIZONTAL)
                replaceBsI2.SetMinSize(wx.Size(-1, 20))
                # 标题
                replaceLabelI2 = wx.StaticText(self, wx.ID_ANY, str(i*2 + 2), wx.DefaultPosition, wx.DefaultSize, 0)
                replaceBsI2.Add(replaceLabelI2, 0, wx.ALL, 5)
                # TextCtrl
                replaceFilePathI2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(1000, -1), 0)
                replaceFilePathI2.Bind(wx.EVT_KEY_DOWN, self.TextCtrlEnterDown)
                self.replaceFilePaths.append(replaceFilePathI2)

                replaceBsI2.Add(replaceFilePathI2, 0, wx.ALL, 5)
                gSizer.Add(replaceBsI2, 1, wx.EXPAND, 5)

            replaceBsWrapper.Add(gSizer, 1, wx.EXPAND, 5)

        # 底部操作按钮
        Btns = wx.BoxSizer(wx.HORIZONTAL)
        Btns.SetMinSize(wx.Size(-1, 20))
        self.btn1 = wx.Button(self, 2001, '清空并生成目录', wx.DefaultPosition, wx.DefaultSize, 0)
        Btns.Add(self.btn1, 0, wx.ALL, 5)
        self.btn2 = wx.Button(self, 2002, '追加在原有目录', wx.DefaultPosition, wx.DefaultSize, 0)
        Btns.Add(self.btn2, 0, wx.ALL, 5)
        self.btn3 = wx.Button(self, 2003, '重置', wx.DefaultPosition, wx.DefaultSize, 0)
        Btns.Add(self.btn3, 0, wx.ALL, 5)
        self.btn4 = wx.Button(self, 2004, '追加并生成新目录', wx.DefaultPosition, wx.DefaultSize, 0)
        Btns.Add(self.btn4, 0, wx.ALL, 5)
        self.notify = wx.StaticText(self, wx.ID_ANY, '', wx.DefaultPosition, wx.DefaultSize, 0)
        self.notify.Wrap(-1)
        self.notify.SetMinSize(wx.Size(260, -1))
        Btns.Add(self.notify, 0, wx.ALL, 5)
        replaceBsWrapper.Add(Btns, 1, wx.EXPAND, 5)

        self.SetSizer(replaceBsWrapper)
        self.Layout()

        self.Centre(wx.BOTH)

        # 绑定事件
        self.btn1.Bind(wx.EVT_BUTTON, self.generate)
        self.btn2.Bind(wx.EVT_BUTTON, self.generate)
        self.btn3.Bind(wx.EVT_BUTTON, self.reset)
        self.btn4.Bind(wx.EVT_BUTTON, self.generateNewFolder)
        # 更新事件
        pub.subscribe(self.FocusNextTextCtrl, 'UpdateFocusTextCtrl')

    # 应对替换jar的情况
    def choose_project(self, event):
        label = event.GetEventObject().GetLabelText()
        self.st_project.SetLabel(label)
        self.project_name = label

    def create_project_btn(self, name, bind_func, wx_id):
        self.project_btn1 = wx.Button(self, wx_id, name, wx.DefaultPosition, wx.DefaultSize, 0)
        self.project_btn1.Bind(wx.EVT_BUTTON, bind_func)
        self.project_btns.Add(self.project_btn1, 0, wx.ALL, 5)

    def generate(self, event):
        self.get_target_files(event, structure_path)

    def reset(self, event):
        for pathTC in self.replaceFilePaths:
            pathTC.SetValue('')

    def generateNewFolder(self, event):
        datetime_str = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-')
        self.get_target_files(event, structure_path, datetime_str)

    # 回车自动触发 文件地址输入
    def TextCtrlEnterDown(self, event):
        index = self.replaceFilePaths.index(event.GetEventObject())
        if event.GetKeyCode() == 370 or event.GetKeyCode() == 13:
            try:
                value = int(event.GetEventObject().GetValue())
                if 1 <= value <= 10:
                    num = 0
                    if 1 <= value <= 9:
                        num = value
                    elif value == 10:
                        num = 0
                    event.GetEventObject().SetValue('')
                    self.FocusNextTextCtrl(value, index, num)

            except Exception:
                print(Exception)

        elif event.GetKeyCode() == 9:
            self.FocusNextTextCtrl(0, index + 1)
        event.Skip()

    # 焦点切换至下一个 TextCtrl
    def FocusNextTextCtrl(self, value, index, num=None):
        if index < size:
            self.replaceFilePaths[index].SetFocus()
        else:
            self.replaceFilePaths[0].SetFocus()
        if index < size and value > 0 and num is not None:
            pyautogui.hotkey('ctrlleft', 'winleft', 'num%s' % num)
            value -= 1
            threading.Timer(0.05, self.UpdateFocusTextCtrl, (value, index + 1, num)).start()

    def UpdateFocusTextCtrl(self, value, index, num):
        wx.CallAfter(pub.sendMessage, 'UpdateFocusTextCtrl', value=value, index=index, num=num)

    # wx弹窗
    def Info(self, message, caption):
        dlg = wx.MessageDialog(self, message, caption, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    # 获得编译后的目标文件
    def get_target_files(self, event, structure_path, datetime_str=''):
        file = open('conf-%s.yaml' % getpass.getuser(), 'r', encoding='UTF-8')
        local_project_config = yaml.load(file)
        source_file_path_list = []

        for pathTC in self.replaceFilePaths:
            if pathTC.GetValue():
                source_file_path_list.append(pathTC.GetValue())

        # 清理jar的抽取目录
        if os.path.exists(jar_extract_path):
            shutil.rmtree(jar_extract_path)
        # 删除已存在的目录，只有2001有删除
        if event.GetId() == 2001:
            if os.path.exists(structure_path):
                shutil.rmtree(structure_path)

        # 生成目录结构
        target_files = {}
        for source_file_path in source_file_path_list:
            for (name, obj) in local_project_config.items():
                # 编译前源代码路径
                source_location = obj['source_location']  # 示例 D:\IdeaSource\Glodon\java\gcj_dws_hw
                # 编译后路径前缀
                compiled_location = obj['compiled_location']  # 示例 E:\Works\Publication Directory\gcj_dws_hw_online
                # 编译后工程名
                compiled_project_name = str(compiled_location).split('\\')[-1]  # 示例 gcj_dws_hw_online

                # 根据源代码路径获得 编译后的文件路径
                if str(source_file_path).find('\\src\\main\\') != -1:
                    _file = source_file_path.split('\\src\\main\\')
                    # 源代码路径前缀
                    src_file_header_path = _file[0]  # 示例 D:\IdeaSource\Glodon\java\gcj_dws_hw
                    # 源代码相对路径
                    src_file_ref_path = _file[1]  # 示例 java\com\gcj\service\rds\StartJobService.java

                    if src_file_header_path == source_location:
                        # class文件
                        if src_file_ref_path.startswith('java'):
                            compiled_ref_filepath = src_file_ref_path.replace('java\\', '').replace('.java', '.class')
                            compiled_file_path = compiled_location + "\\WEB-INF\\classes\\%s" % compiled_ref_filepath
                            target_files[compiled_file_path] = {
                                "compiled_project_name": compiled_project_name,
                                "des_ref_file_name": '\\' + compiled_project_name + "\\WEB-INF\\classes\\%s" % compiled_ref_filepath
                            }

                        # resource文件
                        if src_file_ref_path.startswith('resource'):
                            compiled_ref_filepath = src_file_ref_path.replace('resources\\', '')
                            # compiled_file_path = compiled_location + "\\WEB-INF\\classes\\%s" % compiled_ref_filepath
                            # target_files[compiled_file_path] = '\\' + compiled_project_name + "\\WEB-INF\\classes\\%s" % compiled_ref_filepath
                            target_files[source_file_path] = {
                                "compiled_project_name": compiled_project_name,
                                "des_ref_file_name": '\\' + compiled_project_name + "\\WEB-INF\\classes\\%s" % compiled_ref_filepath
                            }
                        # web文件
                        if src_file_ref_path.startswith('webapp'):
                            compiled_ref_filepath = src_file_ref_path.replace('webapp\\', '')
                            # compiled_file_path = compiled_location + "\\%s" % compiled_ref_filepath
                            # target_files[compiled_file_path] = '\\' + compiled_project_name + "\\%s" % compiled_ref_filepath
                            target_files[source_file_path] = {
                                "compiled_project_name": compiled_project_name,
                                "des_ref_file_name": '\\' + compiled_project_name + "\\%s" % compiled_ref_filepath
                            }
                # jar包
                else:
                    if not self.project_name:
                        self.Info("替换jar 必须要选择工程", caption='提示')
                        return
                    if (self.project_name == name) & str(source_file_path).endswith('.jar'):
                        des_ref_file_name = '\\' + compiled_project_name + '\\WEB-INF\\lib\\' + os.path.basename(source_file_path)
                        target_files[source_file_path] = {
                            "compiled_project_name": compiled_project_name,
                            "des_ref_file_name": des_ref_file_name
                        }

        self.gen_replace_project(target_files)

        # 追加并生成新目录：生成新目录
        if event.GetId() == 2004:
            self.gen_replace_project(target_files, datetime_str)

        # 清理jar的抽取目录
        if os.path.exists(jar_extract_path):
            shutil.rmtree(jar_extract_path)
        self.notify.SetLabel('已生成')
        os.system("explorer.exe %s" % structure_path)

    # 生成替换工程
    def gen_replace_project(self, target_files, datetime_str=''):
        if len(target_files) > 0:
            # compiled_file_path    E:\Works\Publication Directory\gcj_dws_hw_online\WEB-INF\classes\com\gcj\batch\JDBCWriter.class
            # des_ref_file_name     \gcj_dws_hw_online\WEB-INF\classes\com\gcj\batch\JDBCWriter.class
            # compiled_project_name gcj_dws_hw_online
            # compiled_file_path    E:\.m2\repository\glodon\member\center\member-center-util\1.0.0-SNAPSHOT\member-center-util-1.0.0-20180330.020038-149.jar
            # des_ref_file_name     \gcj_dws_hw_online\WEB-INF\lib\member-center-util-1.0.0-20180330.020038-149.jar
            for (compiled_file_path, object) in target_files.items():
                des_ref_file_name = object['des_ref_file_name']
                compiled_project_name = object['compiled_project_name']

                # 如果是生成新路径，则以时间戳命名文件夹
                des_ref_file_name = des_ref_file_name.replace('\\', '\\%s' % datetime_str, 1)
                # 最终保存路径
                copy_file(compiled_file_path, structure_path + des_ref_file_name)

                # 检查是否需要解压jar
                if extract.get(compiled_project_name) and str(compiled_file_path).endswith('.jar'):
                    for extract_jar_prefix in extract[object['compiled_project_name']]:
                        if os.path.basename(compiled_file_path).startswith(extract_jar_prefix):
                            # 解压后文件所在目录
                            extract_jar_dir = un_zip(compiled_file_path, jar_extract_path)
                            # 拷贝 **/*.xml,**/*.properties*,**/*.class
                            for filepath in glob.glob(extract_jar_dir + '\\**\\*', recursive=True):
                                include = filepath.find('.properties') != -1 or filepath.endswith('.xml') or filepath.endswith('.class')
                                exclude = os.path.basename(filepath) == 'pom.xml'
                                if include and not exclude:
                                    extract_class_ref_filename = filepath.replace(extract_jar_dir, '')
                                    copy_file(filepath, structure_path + '\\' + compiled_project_name + '\\WEB-INF\\classes\\' + extract_class_ref_filename)

        for filename in glob.glob(structure_path + '\\**\\*', recursive=True):
            if filename.endswith('.huawei-beijing.online'):
                copy_file(filename, filename.replace('.huawei-beijing.online', ''))

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None).Show()
    app.MainLoop()
