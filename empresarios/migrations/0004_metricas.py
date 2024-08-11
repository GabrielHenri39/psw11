# Generated by Django 5.0.7 on 2024-08-10 18:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresarios', '0003_documento'),
    ]

    operations = [
        migrations.CreateModel(
            name='Metricas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=30)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='empresarios.empresas')),
            ],
            options={
                'verbose_name_plural': 'Metricas',
            },
        ),
    ]
