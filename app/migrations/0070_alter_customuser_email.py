# Generated by Django 3.2 on 2021-12-02 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0069_auto_20211202_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='Email'),
        ),
    ]