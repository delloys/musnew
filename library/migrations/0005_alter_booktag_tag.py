# Generated by Django 4.2.1 on 2023-05-30 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_alter_bookauthor_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booktag',
            name='tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bt_id_tag', to='library.tag'),
        ),
    ]
