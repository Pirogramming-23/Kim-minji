# Generated by Django 5.2.4 on 2025-07-21 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_remove_post_image_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(default='제목 없음', max_length=100),
        ),
    ]
