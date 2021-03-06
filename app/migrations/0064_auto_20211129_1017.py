# Generated by Django 3.2 on 2021-11-29 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0063_auto_20211129_0044'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentos_inscripcion',
            name='esta_aprovado',
            field=models.BooleanField(default=False, verbose_name='Estado de aprovado'),
        ),
        migrations.CreateModel(
            name='documentos_inscripcion_revision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('esta_aprovado', models.BooleanField(default=False, verbose_name='Estado de aprovado')),
                ('id_administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.administrador')),
                ('id_documento_inscripcion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.documentos_inscripcion')),
            ],
            options={
                'verbose_name': 'Documento de Inscripcion - Revision',
                'verbose_name_plural': 'Documentos de Inscripcion - Revision',
                'ordering': ['id'],
            },
        ),
    ]
