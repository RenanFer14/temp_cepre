# Generated by Django 3.2 on 2021-11-08 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_auto_20211108_2236'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pabellon',
            old_name='denominacion_pabellon',
            new_name='nombre_pabellon',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='categoria',
        ),
        migrations.AddField(
            model_name='aula',
            name='codigo_aula',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Codigo de aula'),
        ),
        migrations.AddField(
            model_name='aula',
            name='sillas_fijas',
            field=models.PositiveIntegerField(default=0, verbose_name='Nro. de sillas fijas'),
        ),
        migrations.AddField(
            model_name='aula',
            name='sillas_moviles',
            field=models.PositiveIntegerField(default=0, verbose_name='Nro. de sillas moviles'),
        ),
        migrations.AddField(
            model_name='docente',
            name='regimen_docente',
            field=models.CharField(blank=True, choices=[('P', 'Principal'), ('L', 'Locador'), ('A', 'Auxiliar'), ('C', 'Contratado')], max_length=3, null=True, verbose_name='Categoria Docente'),
        ),
        migrations.AddField(
            model_name='escuela_profesional',
            name='codigo_escuela',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Codigo'),
        ),
        migrations.AddField(
            model_name='pabellon',
            name='codigo_pabellon',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Codigo pabellon'),
        ),
        migrations.AddField(
            model_name='sede',
            name='direccion',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Direccion'),
        ),
        migrations.AlterField(
            model_name='aula',
            name='capacidad',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Capacidad'),
        ),
        migrations.AlterField(
            model_name='aula',
            name='piso',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Piso'),
        ),
        migrations.AlterField(
            model_name='detalle_compromiso_de_pago',
            name='numero_cuota',
            field=models.PositiveIntegerField(verbose_name='Nro. Cuota'),
        ),
        migrations.AlterField(
            model_name='detalle_pago',
            name='nro_cuota',
            field=models.PositiveIntegerField(verbose_name='Nro. de cuota'),
        ),
        migrations.AlterField(
            model_name='docente',
            name='email_institucional',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Correo Institucional'),
        ),
        migrations.AlterField(
            model_name='docente',
            name='id_persona',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.persona'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='tema_personalizado',
            field=models.PositiveIntegerField(default=1, verbose_name='Tema personalizado'),
        ),
        migrations.AlterField(
            model_name='examen',
            name='nro_examen',
            field=models.PositiveIntegerField(verbose_name='Nro. de examen'),
        ),
        migrations.AlterField(
            model_name='pabellon',
            name='numero_pisos',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Nro. de Pisos'),
        ),
        migrations.AlterField(
            model_name='padron_cursos_grupo',
            name='hora_semana',
            field=models.PositiveIntegerField(verbose_name='Horas a la semana'),
        ),
        migrations.AlterField(
            model_name='pago',
            name='nro_cuotas',
            field=models.PositiveIntegerField(verbose_name='Nro. de cuota(s)'),
        ),
    ]