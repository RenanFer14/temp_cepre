# Generated by Django 3.2 on 2021-11-16 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0050_auto_20211115_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistencia_estudiante',
            name='estado_asistencia',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='examen',
            name='tipo_examen',
            field=models.CharField(choices=[('PARCIAL', 'Parcial'), ('SIMULACRO', 'Simulacro')], max_length=20, verbose_name='Tipo de examen'),
        ),
    ]
