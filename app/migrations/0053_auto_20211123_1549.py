# Generated by Django 3.2 on 2021-11-23 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0052_remove_persona_digito_verificador'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ubigeo',
            old_name='codigo_ubigeo',
            new_name='codigo',
        ),
        migrations.RenameField(
            model_name='ubigeo',
            old_name='tipo_ubigeo',
            new_name='tipo',
        ),
    ]