# Generated by Django 2.1 on 2018-08-17 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localgaap', '0009_auto_20180815_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='difference',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=16),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='local',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=16, verbose_name='Local GAAP value'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='neutral_movement',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=16),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='permanent_quota',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=7),
        ),
    ]