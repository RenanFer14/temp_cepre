# Generated by Django 3.2 on 2021-10-21 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alter_pago_tipo_colegio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compromiso_pago',
            name='id_preinscripcion',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.preinscripcion'),
        ),
    ]