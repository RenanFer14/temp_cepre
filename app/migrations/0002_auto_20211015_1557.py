# Generated by Django 3.2 on 2021-10-15 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estudiante',
            name='correo_institucional',
        ),
        migrations.RemoveField(
            model_name='estudiante',
            name='password',
        ),
        migrations.AddField(
            model_name='estudiante',
            name='tema_personalizado',
            field=models.IntegerField(default=1, verbose_name='Tema personalizado'),
        ),
    ]
