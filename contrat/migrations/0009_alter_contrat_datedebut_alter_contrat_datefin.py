# Generated by Django 5.1.1 on 2024-10-02 14:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contrat', '0008_contrat_termes_du_contrat_alter_contrat_datedebut_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrat',
            name='datedebut',
            field=models.DateField(default=datetime.datetime(2024, 10, 2, 16, 16, 5, 531850)),
        ),
        migrations.AlterField(
            model_name='contrat',
            name='datefin',
            field=models.DateField(default=datetime.datetime(2024, 10, 2, 16, 16, 5, 531850)),
        ),
    ]
