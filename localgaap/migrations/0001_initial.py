# Generated by Django 2.0.7 on 2018-07-04 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_version_locked'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oar', models.CharField(max_length=32, verbose_name='Reference')),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(default='Other', max_length=20)),
                ('local', models.DecimalField(decimal_places=2, default=0, max_digits=16, verbose_name='Local GAAP value')),
                ('difference', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('neutral_movement', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Version')),
            ],
        ),
    ]
