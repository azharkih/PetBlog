# Generated by Django 2.2.6 on 2020-12-06 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20201202_1106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='follower',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, help_text='Выберите изображение к сообщению', null=True, upload_to='posts/', verbose_name='Изображение'),
        ),
    ]
