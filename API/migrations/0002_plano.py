# Generated by Django 4.1.6 on 2023-06-26 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plano',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('imagen', models.ImageField(upload_to='almacen/')),
                ('pasillos', models.IntegerField()),
                ('secciones', models.IntegerField()),
                ('alturas', models.IntegerField()),
            ],
        ),
    ]
