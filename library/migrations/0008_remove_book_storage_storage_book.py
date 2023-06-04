# Generated by Django 4.2.1 on 2023-06-01 00:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_book_storage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='storage',
        ),
        migrations.AddField(
            model_name='storage',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='id_type', to='library.book'),
        ),
    ]