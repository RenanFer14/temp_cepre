# Generated by Django 3.2 on 2021-11-14 14:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0047_alter_escuela_profesional_id_grupo_academico'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistencia_docente',
            name='fecha_sesion',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Fecha registro'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='asistencia_docente',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro'),
        ),
    ]
