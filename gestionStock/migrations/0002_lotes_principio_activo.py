# Generated by Django 3.2.8 on 2021-11-25 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionStock', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lotes',
            name='principio_activo',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
