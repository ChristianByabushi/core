# Generated by Django 5.1.1 on 2024-10-01 10:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contrat', '0003_alter_contrat_datedebut_alter_contrat_datefin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrat',
            name='datedebut',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 1, 12, 5, 50, 978577)),
        ),
        migrations.AlterField(
            model_name='contrat',
            name='datefin',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 1, 12, 5, 50, 978577)),
        ),
    ]
