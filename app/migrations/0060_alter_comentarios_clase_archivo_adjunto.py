# Generated by Django 3.2 on 2021-11-26 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0059_docente_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentarios_clase',
            name='archivo_adjunto',
            field=models.FileField(blank=True, null=True, upload_to='archivos_clase', verbose_name='Archivo adjunto'),
        ),
    ]
