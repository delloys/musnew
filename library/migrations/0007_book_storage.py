# Generated by Django 4.2.1 on 2023-06-01 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_alter_book_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='storage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='id_storage', to='library.storage'),
        ),
    ]
