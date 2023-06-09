# Generated by Django 3.2.4 on 2022-10-19 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cartoon_menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_show', models.BooleanField(default=False, verbose_name='是否显示')),
                ('orders', models.IntegerField(default=1, verbose_name='排序')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='动漫名称')),
                ('img_url', models.CharField(max_length=1000, verbose_name='图片地址')),
                ('note', models.CharField(max_length=100, verbose_name='更新状态')),
                ('href', models.CharField(max_length=1000, verbose_name='详情页面')),
            ],
            options={
                'verbose_name': '课程分类',
                'verbose_name_plural': '课程分类',
                'db_table': 'ly_course_category',
            },
        ),
    ]
