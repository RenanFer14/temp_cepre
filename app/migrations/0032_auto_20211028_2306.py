# Generated by Django 3.2 on 2021-10-28 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_auto_20211028_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='ciclo',
            name='turno_mañana',
            field=models.BooleanField(default=False, verbose_name='Turno Mañana'),
        ),
        migrations.AddField(
            model_name='ciclo',
            name='turno_noche',
            field=models.BooleanField(default=False, verbose_name='Turno Noche'),
        ),
        migrations.AddField(
            model_name='ciclo',
            name='turno_tarde',
            field=models.BooleanField(default=False, verbose_name='Turno Tarde'),
        ),
        migrations.AddField(
            model_name='pago',
            name='turno_pago',
            field=models.CharField(max_length=10, null=True, verbose_name='Turno'),
        ),
    ]