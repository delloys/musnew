# Generated by Django 4.2.1 on 2023-06-06 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artefacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artefact',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]