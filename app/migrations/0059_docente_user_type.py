# Generated by Django 3.2 on 2021-11-26 00:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0058_auto_20211126_0013'),
    ]

    operations = [
        migrations.AddField(
            model_name='docente',
            name='user_type',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.customuser', verbose_name='DNI'),
            preserve_default=False,
        ),
    ]
