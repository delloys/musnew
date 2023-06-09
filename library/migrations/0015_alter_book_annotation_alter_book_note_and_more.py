# Generated by Django 4.2.1 on 2023-06-07 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_alter_book_annotation_alter_book_note_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='annotation',
            field=models.TextField(blank=True, default='-', null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='note',
            field=models.TextField(blank=True, default='-', null=True),
        ),
        migrations.AlterField(
            model_name='copy',
            name='part',
            field=models.CharField(blank=True, default='-', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='copy',
            name='release',
            field=models.CharField(blank=True, default='-', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='storage',
            name='closet',
            field=models.CharField(blank=True, default='-', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='storage',
            name='link',
            field=models.TextField(blank=True, default='-', null=True),
        ),
        migrations.AlterField(
            model_name='storage',
            name='shelf',
            field=models.CharField(blank=True, default='-', max_length=20, null=True),
        ),
    ]
