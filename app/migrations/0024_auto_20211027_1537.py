# Generated by Django 3.2 on 2021-10-27 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_auto_20211027_1518'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalle_pago',
            name='monto_mora_privado',
        ),
        migrations.RemoveField(
            model_name='detalle_pago',
            name='monto_mora_publico',
        ),
        migrations.RemoveField(
            model_name='detalle_pago',
            name='monto_parcial_privado',
        ),
        migrations.RemoveField(
            model_name='detalle_pago',
            name='monto_parcial_publico',
        ),
        migrations.RemoveField(
            model_name='pago',
            name='monto_total_privado',
        ),
        migrations.RemoveField(
            model_name='pago',
            name='monto_total_publico',
        ),
        migrations.AddField(
            model_name='detalle_pago',
            name='monto_mora',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Valor'),
        ),
        migrations.AddField(
            model_name='detalle_pago',
            name='monto_parcial',
            field=models.DecimalField(decimal_places=2, default=131, max_digits=10, verbose_name='Monto Parcial'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pago',
            name='monto_total',
            field=models.DecimalField(decimal_places=2, default=313, max_digits=10, verbose_name='Monto Total'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='registro_tesoreria',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='registro_tesoreria',
            name='id_detalle_compromiso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.detalle_compromiso_de_pago'),
        ),
    ]
