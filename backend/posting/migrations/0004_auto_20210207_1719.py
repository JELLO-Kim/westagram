# Generated by Django 3.1.5 on 2021-02-07 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0003_auto_20210205_0151'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='posting',
        ),
    ]