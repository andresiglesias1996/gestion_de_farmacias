# Generated by Django 3.2.8 on 2021-11-25 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionUsuarios', '0002_auto_20211125_1027'),
        ('gestionStock', '0004_auto_20211125_1848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lotes',
            name='destinatario',
        ),
        migrations.AddField(
            model_name='lotes',
            name='receta_de_destino',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receta_de_destino', to='gestionUsuarios.recetas'),
        ),
    ]
