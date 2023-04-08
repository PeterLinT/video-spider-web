import os
import sys
sys.path.append(os.path.dirname(os.path.abspath('')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'mutefuncopy.settings'    # 项目名.settings
import django
django.setup()

"""
import django
import os
import sys

# 将django的项目路径加入到当前的环境
sys.path.insert(0, os.path.dirname(os.getcwd()))

# django项目舒适化
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

django.setup()
"""