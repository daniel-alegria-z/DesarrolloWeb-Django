# Generated by Django 5.1.1 on 2024-11-22 21:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreCompleto', models.CharField(max_length=30)),
                ('rol', models.CharField(max_length=30)),
                ('contrasena', models.CharField(default='123', max_length=128)),
                ('ano_nacimiento', models.CharField(default='123', max_length=30)),
                ('pais', models.CharField(max_length=30)),
                ('telefono', models.CharField(max_length=30)),
                ('correo', models.CharField(max_length=30)),
                ('genero', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioBorrado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreCompleto', models.CharField(max_length=30)),
                ('rol', models.CharField(max_length=30)),
                ('contrasena', models.CharField(default='123', max_length=128)),
                ('ano_nacimiento', models.CharField(default='123', max_length=30)),
                ('pais', models.CharField(max_length=30)),
                ('telefono', models.CharField(max_length=30)),
                ('correo', models.CharField(max_length=30)),
                ('genero', models.CharField(default='', max_length=30)),
                ('fecha_eliminacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransporteBorrado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idTransporte', models.IntegerField()),
                ('empresaTransporte', models.CharField(max_length=30)),
                ('medioTransporte', models.CharField(max_length=30)),
                ('numeroMatricula', models.CharField(max_length=30)),
                ('conductor', models.CharField(max_length=40)),
                ('ruta', models.CharField(max_length=40)),
                ('fechaSalida', models.CharField()),
                ('fechaLlegada', models.CharField()),
                ('estadoTransporte', models.CharField(max_length=40)),
                ('fecha_eliminacion', models.DateTimeField(auto_now_add=True)),
                ('responsableID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Transporte',
            fields=[
                ('idTransporte', models.IntegerField(help_text='ID unico para el tipo', primary_key=True, serialize=False)),
                ('empresaTransporte', models.CharField(max_length=30)),
                ('medioTransporte', models.CharField(max_length=30)),
                ('numeroMatricula', models.CharField(max_length=30)),
                ('conductor', models.CharField(max_length=40)),
                ('ruta', models.CharField(max_length=40)),
                ('fechaSalida', models.CharField()),
                ('fechaLlegada', models.CharField()),
                ('estadoTransporte', models.CharField(max_length=40)),
                ('responsableID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='ImportacionBorrada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idImportacion', models.IntegerField()),
                ('fechaDeclaracion', models.CharField()),
                ('proveedor', models.CharField(max_length=30)),
                ('descripcionMercancia', models.CharField(max_length=100)),
                ('codigoArancelario', models.BigIntegerField()),
                ('cantidad', models.IntegerField()),
                ('unidadMedida', models.CharField(max_length=30)),
                ('valorCif', models.FloatField()),
                ('impuestos', models.FloatField()),
                ('origenMercancia', models.CharField(max_length=30)),
                ('puertoEntrada', models.CharField(max_length=30)),
                ('fecha_eliminacion', models.DateTimeField(auto_now_add=True)),
                ('transporteID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.transporte')),
                ('responsableID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Importacion',
            fields=[
                ('idImportacion', models.IntegerField(help_text='ID unico para el tipo', primary_key=True, serialize=False)),
                ('fechaDeclaracion', models.CharField()),
                ('proveedor', models.CharField(max_length=30)),
                ('descripcionMercancia', models.CharField(max_length=100)),
                ('codigoArancelario', models.BigIntegerField()),
                ('cantidad', models.IntegerField()),
                ('unidadMedida', models.CharField(max_length=30)),
                ('valorCif', models.FloatField()),
                ('impuestos', models.FloatField()),
                ('origenMercancia', models.CharField(max_length=30)),
                ('puertoEntrada', models.CharField(max_length=30)),
                ('transporteID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.transporte')),
                ('responsableID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='ExportacionBorrada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idExportacion', models.IntegerField()),
                ('fechaDeclaracion', models.CharField()),
                ('cliente', models.CharField(max_length=30)),
                ('descripcionMercancia', models.CharField(max_length=100)),
                ('codigoArancelario', models.BigIntegerField()),
                ('cantidad', models.IntegerField()),
                ('unidadMedida', models.CharField(max_length=30)),
                ('valorFob', models.IntegerField()),
                ('impuestos', models.CharField(max_length=30)),
                ('destinoMercancia', models.CharField(max_length=30)),
                ('puertoSalida', models.CharField(max_length=30)),
                ('fecha_eliminacion', models.DateTimeField(auto_now_add=True)),
                ('transporteID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.transporte')),
                ('responsableID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Exportacion',
            fields=[
                ('idExportacion', models.IntegerField(help_text='ID unico para el tipo', primary_key=True, serialize=False)),
                ('fechaDeclaracion', models.CharField()),
                ('cliente', models.CharField(max_length=30)),
                ('descripcionMercancia', models.CharField(max_length=100)),
                ('codigoArancelario', models.BigIntegerField()),
                ('cantidad', models.IntegerField()),
                ('unidadMedida', models.CharField(max_length=30)),
                ('valorFob', models.FloatField()),
                ('impuestos', models.CharField(max_length=30)),
                ('destinoMercancia', models.CharField(max_length=30)),
                ('puertoSalida', models.CharField(max_length=30)),
                ('transporteID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.transporte')),
                ('responsableID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='ControlBorrado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idControl', models.IntegerField()),
                ('fechaInspeccion', models.CharField()),
                ('horaInspeccion', models.CharField(default='00:00', max_length=20)),
                ('tipoControl', models.CharField(max_length=30)),
                ('resultadoInspeccion', models.CharField(max_length=30)),
                ('descripcionHallazgos', models.CharField(max_length=30)),
                ('fecha_eliminacion', models.DateTimeField(auto_now_add=True)),
                ('idExportacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.exportacion')),
                ('idImportacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.importacion')),
                ('responsableID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Control',
            fields=[
                ('idControl', models.IntegerField(help_text='ID unico para el tipo', primary_key=True, serialize=False)),
                ('fechaInspeccion', models.CharField()),
                ('horaInspeccion', models.CharField(default='00:00', max_length=20)),
                ('tipoControl', models.CharField(max_length=30)),
                ('resultadoInspeccion', models.CharField(max_length=30)),
                ('descripcionHallazgos', models.CharField()),
                ('idExportacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.exportacion')),
                ('idImportacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.importacion')),
                ('responsableID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='CargaBorrado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idCarga', models.IntegerField()),
                ('tipoCarga', models.CharField(max_length=30)),
                ('descripcionCarga', models.CharField(max_length=100)),
                ('pesoBruto', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pesoNeto', models.DecimalField(decimal_places=2, max_digits=5)),
                ('volumen', models.DecimalField(decimal_places=2, max_digits=5)),
                ('embalaje', models.CharField(max_length=30)),
                ('contenido', models.CharField(max_length=30)),
                ('valorDeclarado', models.FloatField()),
                ('seguroCarga', models.FloatField()),
                ('estadoCarga', models.CharField(max_length=30)),
                ('fecha_eliminacion', models.DateTimeField(auto_now_add=True)),
                ('idExportacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.exportacion')),
                ('idImportacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.importacion')),
                ('responsableID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Carga',
            fields=[
                ('idCarga', models.IntegerField(help_text='ID unico para el tipo', primary_key=True, serialize=False)),
                ('tipoCarga', models.CharField(max_length=30)),
                ('descripcionCarga', models.CharField(max_length=100)),
                ('pesoBruto', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pesoNeto', models.DecimalField(decimal_places=2, max_digits=5)),
                ('volumen', models.DecimalField(decimal_places=2, max_digits=5)),
                ('embalaje', models.CharField(max_length=30)),
                ('contenido', models.CharField(max_length=30)),
                ('valorDeclarado', models.FloatField()),
                ('seguroCarga', models.FloatField()),
                ('estadoCarga', models.CharField(max_length=30)),
                ('idExportacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.exportacion')),
                ('idImportacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.importacion')),
                ('responsableID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estacion.usuario')),
            ],
        ),
    ]
