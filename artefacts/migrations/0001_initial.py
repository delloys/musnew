# Generated by Django 4.2.1 on 2023-06-06 06:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Culture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_cult', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'culture',
            },
        ),
        migrations.CreateModel(
            name='Ex_lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_ex_lead', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'ex_lead',
            },
        ),
        migrations.CreateModel(
            name='Ex_monument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_ex', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'ex_monument',
            },
        ),
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_hall', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'hall',
            },
        ),
        migrations.CreateModel(
            name='Historical_period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_hist', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'historical_per',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_mat', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'material',
            },
        ),
        migrations.CreateModel(
            name='Museum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_mus', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'museum',
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_place', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'place',
            },
        ),
        migrations.CreateModel(
            name='Year_monument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.DateField()),
            ],
            options={
                'db_table': 'year_monument',
            },
        ),
        migrations.CreateModel(
            name='HistoricalCulture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_cult', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hc_id_cult', to='artefacts.culture')),
                ('name_hist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hc_id_hist', to='artefacts.historical_period')),
            ],
            options={
                'db_table': 'historical_culture',
            },
        ),
        migrations.CreateModel(
            name='HallPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hp_id_hall', to='artefacts.hall')),
                ('name_place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hp_id_place', to='artefacts.place')),
            ],
            options={
                'db_table': 'hall_place_location',
            },
        ),
        migrations.CreateModel(
            name='Artefact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniq_name', models.CharField(max_length=255, unique=True)),
                ('number', models.PositiveBigIntegerField(unique=True)),
                ('name_art', models.CharField(max_length=255, null=True)),
                ('age', models.PositiveBigIntegerField(blank=True, null=True)),
                ('size', models.CharField(blank=True, max_length=20, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('ex_lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_lead_ex', to='artefacts.ex_lead')),
                ('ex_monument', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_ex_monument', to='artefacts.ex_monument')),
                ('histcult', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='id_hist_cult', to='artefacts.historicalculture')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_hall_place', to='artefacts.hallplace')),
                ('material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='id_material', to='artefacts.material')),
                ('museum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_museum', to='artefacts.museum')),
                ('user_last_changes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_year', to='artefacts.year_monument')),
            ],
            options={
                'db_table': 'artefact',
                'get_latest_by': 'last_modified',
            },
        ),
    ]
