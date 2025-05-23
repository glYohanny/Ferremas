# Generated by Django 5.2.1 on 2025-05-09 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TipoCambio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moneda_origen', models.CharField(max_length=3)),
                ('moneda_destino', models.CharField(max_length=3)),
                ('tasa', models.DecimalField(decimal_places=6, max_digits=18)),
                ('fecha_validez', models.DateField()),
                ('fuente', models.CharField(default='No especificada', max_length=100)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Tipo de Cambio',
                'verbose_name_plural': 'Tipos de Cambio',
                'db_table': 'tipo_cambio',
                'ordering': ['-fecha_validez', 'moneda_origen', 'moneda_destino'],
                'indexes': [models.Index(fields=['fecha_validez'], name='tipo_cambio_fecha_v_379b10_idx'), models.Index(fields=['moneda_origen', 'moneda_destino', 'fecha_validez'], name='tipo_cambio_moneda__61b223_idx')],
                'unique_together': {('moneda_origen', 'moneda_destino', 'fecha_validez', 'fuente')},
            },
        ),
    ]
