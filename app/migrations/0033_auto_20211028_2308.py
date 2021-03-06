# Generated by Django 3.2 on 2021-10-28 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_auto_20211028_2306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pago',
            name='turno_pago',
        ),
        migrations.AlterField(
            model_name='ciclo',
            name='turno_mañana',
            field=models.BooleanField(default=False, null=True, verbose_name='Turno Mañana'),
        ),
        migrations.AlterField(
            model_name='ciclo',
            name='turno_noche',
            field=models.BooleanField(default=False, null=True, verbose_name='Turno Noche'),
        ),
        migrations.AlterField(
            model_name='ciclo',
            name='turno_tarde',
            field=models.BooleanField(default=False, null=True, verbose_name='Turno Tarde'),
        ),
    ]
