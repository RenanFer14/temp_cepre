# Generated by Django 3.2 on 2021-11-04 23:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_alter_pago_monto_total'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='detalle_pago',
            unique_together=set(),
        ),
    ]
