# Generated by Django 3.2.4 on 2022-11-30 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fantuan', '0003_alter_tv_play_introduction'),
    ]

    operations = [
        migrations.CreateModel(
            name='tv_video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否显示')),
                ('orders', models.IntegerField(default=1, verbose_name='排序')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('title', models.CharField(max_length=100, verbose_name='电视剧名')),
                ('api_from', models.CharField(max_length=10, unique=True, verbose_name='接口名')),
                ('episode', models.CharField(max_length=10, verbose_name='第几集')),
                ('player_url', models.CharField(blank=True, max_length=1000, null=True, unique=True, verbose_name='播放地址')),
                ('video_url', models.CharField(blank=True, max_length=1000, null=True, unique=True, verbose_name='m3u8地址')),
                ('videoid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fantuan.tv_play', verbose_name='电视剧id')),
            ],
            options={
                'verbose_name': '剧集列表',
                'verbose_name_plural': '剧集列表',
                'db_table': 'tv_video',
            },
        ),
    ]