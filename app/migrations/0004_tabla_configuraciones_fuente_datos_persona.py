# Generated by Django 3.2 on 2021-10-18 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20211016_0538'),
    ]

    operations = [
        migrations.AddField(
            model_name='tabla_configuraciones',
            name='fuente_datos_persona',
            field=models.CharField(choices=[('PIDE', 'Datos PIDE'), ('BDD', 'Base de datos local')], default='PIDE', max_length=10, verbose_name='Importar desde'),
            preserve_default=False,
        ),
    ]