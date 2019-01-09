import os
import datetime

# path = r'E:\Works'
# os.system("explorer.exe %s" % path)


print('E:\\Works\\Publication Directory\\member_center_api'.replace('\\', '\\%s' % datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-'), 1))