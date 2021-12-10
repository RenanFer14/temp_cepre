# Generated by Django 3.2 on 2021-10-27 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20211027_1343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detalle_pago',
            old_name='monto_parcial',
            new_name='monto_parcial_privado',
        ),
        migrations.AddField(
            model_name='detalle_pago',
            name='monto_parcial_publico',
            field=models.DecimalField(decimal_places=2, default=1200, max_digits=10, verbose_name='Monto Parcial Publico'),
            preserve_default=False,
        ),
    ]