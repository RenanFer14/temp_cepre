# Generated by Django 3.2 on 2021-10-27 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_auto_20211027_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='padron_documento_requisito',
            name='documento',
            field=models.FileField(null=True, upload_to='docrequisitos', verbose_name='Subir documento'),
        ),
    ]