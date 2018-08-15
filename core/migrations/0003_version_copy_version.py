# Generated by Django 2.0.7 on 2018-07-07 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_version_locked'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='copy_version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='copied_in', to='core.Version'),
        ),
    ]
