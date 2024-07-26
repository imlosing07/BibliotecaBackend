# Generated by Django 5.0.6 on 2024-07-26 05:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BibliotecaApp', '0004_alter_libro_titulo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserva',
            name='usuarioReserva',
        ),
        migrations.AddField(
            model_name='reserva',
            name='alumnoReserva',
            field=models.ForeignKey(default=74616534, on_delete=django.db.models.deletion.CASCADE, to='BibliotecaApp.alumno'),
            preserve_default=False,
        ),
    ]