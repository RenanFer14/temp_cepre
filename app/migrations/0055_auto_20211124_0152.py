# Generated by Django 3.2 on 2021-11-24 01:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0054_auto_20211123_1651'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ubigeo',
            old_name='codigo',
            new_name='codigo_ubigeo',
        ),
        migrations.RenameField(
            model_name='ubigeo',
            old_name='tipo',
            new_name='tipo_ubigeo',
        ),
    ]