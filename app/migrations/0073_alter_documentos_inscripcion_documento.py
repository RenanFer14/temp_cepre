# Generated by Django 3.2 on 2021-12-09 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0072_examen_grupo_finalizado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentos_inscripcion',
            name='documento',
            field=models.FileField(upload_to='inscrito_files_path', verbose_name='Documentos'),
        ),
    ]
