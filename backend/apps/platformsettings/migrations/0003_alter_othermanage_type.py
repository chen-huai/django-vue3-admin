# Generated by Django 4.0.8 on 2022-10-23 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platformsettings', '0002_lunbotumanage_link_type_alter_lunbotumanage_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='othermanage',
            name='type',
            field=models.IntegerField(choices=[(1, '正常值'), (2, '富文本'), (3, '图片'), (4, '视频')], default=1, verbose_name='类型'),
        ),
    ]