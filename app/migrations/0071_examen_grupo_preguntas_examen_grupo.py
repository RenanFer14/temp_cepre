# Generated by Django 3.2 on 2021-12-03 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0070_alter_customuser_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='examen_grupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('id_examen', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.examen')),
                ('id_grupo_academico', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.grupo_academico')),
            ],
            options={
                'verbose_name': 'Examen por grupo',
                'verbose_name_plural': 'Examenes por grupo',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='preguntas_examen_grupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('id_balota_curso', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.balota_preguntas_curso')),
                ('id_examen_grupo', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.examen_grupo')),
            ],
            options={
                'verbose_name': 'Pregunta examen',
                'verbose_name_plural': 'Preguntas examen',
            },
        ),
    ]
