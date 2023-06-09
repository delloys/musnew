# Generated by Django 4.2.1 on 2023-06-07 01:20

import artefacts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artefacts', '0002_alter_artefact_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artefact',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=artefacts.models.UploadToPathAndRename('images/')),
        ),
    ]
