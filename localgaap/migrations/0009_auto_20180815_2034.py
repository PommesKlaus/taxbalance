# Generated by Django 2.0.7 on 2018-08-15 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localgaap', '0008_auto_20180815_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='oar',
            field=models.CharField(blank=True, max_length=32, verbose_name='Reference'),
        ),
    ]
