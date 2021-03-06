# Generated by Django 3.2 on 2021-10-20 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_preinscripcion_id_ubigeo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tabla_configuraciones',
            options={'verbose_name': 'Configuracion', 'verbose_name_plural': 'Configuraciones'},
        ),
        migrations.RemoveField(
            model_name='inscripcion',
            name='documentos',
        ),
        migrations.CreateModel(
            name='documentos_inscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('nombre_documento', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre')),
                ('documento', models.FileField(upload_to='cargar_documentos', verbose_name='Documentos')),
                ('id_inscripcion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.inscripcion')),
            ],
            options={
                'verbose_name_plural': 'Documentos de Inscripcion',
            },
        ),
    ]
