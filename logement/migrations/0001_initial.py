# Generated by Django 5.1.1 on 2024-10-01 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adresse', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('salle', 'Salle'), ('appartement', 'Appartement'), ('Maison', 'maison'), ('terrain', 'Terrain')], max_length=50)),
                ('surface', models.CharField(max_length=50)),
                ('disponible', models.BooleanField(default=True)),
            ],
        ),
    ]
