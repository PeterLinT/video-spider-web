from django.contrib import admin

from .models import cartoon_menu


# Register your models here.

class CartoonMenuAdmin(admin.ModelAdmin):
    # 设置列表可显示的字段
    list_display = ('id','title', 'img_url', 'note','href','updated_time')
    # 设置过滤选项
    list_filter = ('id', 'updated_time')


admin.site.register(cartoon_menu, CartoonMenuAdmin)
