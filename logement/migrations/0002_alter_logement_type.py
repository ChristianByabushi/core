# Generated by Django 5.1.1 on 2024-10-02 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logement',
            name='type',
            field=models.CharField(choices=[('salle', 'Salle'), ('appartement', 'Appartement'), ('maison', 'Maison'), ('terrain', 'Terrain')], max_length=50),
        ),
    ]
