# Generated by Django 5.0.6 on 2024-07-26 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BibliotecaApp', '0003_remove_libro_id_alter_libro_isbn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='titulo',
            field=models.CharField(max_length=150),
        ),
    ]