# Generated by Django 4.1.1 on 2022-09-14 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_PWD_Management', '0003_rename_pwd_userpassword_passwords'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpassword',
            old_name='passwords',
            new_name='password',
        ),
    ]
