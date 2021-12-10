# Generated by Django 3.2 on 2021-10-18 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_persona_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='lugar_nacimiento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ubigeo', verbose_name='Lugar de nacimiento'),
        ),
        migrations.AlterField(
            model_name='preinscripcion',
            name='id_ubigeo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ubigeo', verbose_name='Lugar actual de residencia'),
        ),
    ]