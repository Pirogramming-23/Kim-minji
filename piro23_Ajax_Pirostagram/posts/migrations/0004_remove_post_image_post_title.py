# Generated by Django 5.2.4 on 2025-07-21 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_postimage_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='제목 없음', max_length=100),
            preserve_default=False,
        ),
    ]
