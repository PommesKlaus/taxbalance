# Generated by Django 2.0.7 on 2018-07-06 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_version_locked'),
        ('localgaap', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='transaction',
            unique_together={('version', 'oar')},
        ),
    ]