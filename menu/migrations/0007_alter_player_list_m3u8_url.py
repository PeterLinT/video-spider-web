# Generated by Django 3.2.4 on 2022-10-19 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_player_list_m3u8_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player_list',
            name='m3u8_url',
            field=models.CharField(blank=True, max_length=1000, null=True, unique=True, verbose_name='m3u8地址'),
        ),
    ]
