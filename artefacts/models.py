import os
from django.conf import settings
from django.db import models
from django.utils.deconstruct import deconstructible
from django.core.files.storage import default_storage


# Create your models here.
class Museum(models.Model):
    name_mus = models.CharField(max_length=10)

    class Meta:
        db_table = 'museum'

    def __str__(self):
        return self.name_mus

class Ex_monument(models.Model):
    name_ex = models.CharField(max_length=255)

    class Meta:
        db_table = 'ex_monument'

    def __str__(self):
        return self.name_ex


class Year_monument(models.Model):
    year = models.CharField(max_length=4)

    class Meta:
        db_table = 'year_monument'

    def __str__(self):
        return self.year


class Material(models.Model):
    name_mat = models.CharField(max_length=255)

    class Meta:
        db_table = 'material'

    def __str__(self):
        return self.name_mat

class Culture(models.Model):
    name_cult = models.CharField(max_length=255)

    class Meta:
        db_table = 'culture'

    def __str__(self):
        return self.name_cult


class Historical_period(models.Model):
    name_hist = models.CharField(max_length=255)

    class Meta:
        db_table = 'historical_per'

    def __str__(self):
        return self.name_hist


class Ex_lead(models.Model):
    name_ex_lead = models.CharField(max_length=255)

    class Meta:
        db_table = 'ex_lead'

    def __str__(self):
        return self.name_ex_lead


class Hall(models.Model):
    name_hall = models.CharField(max_length=255)

    class Meta:
        db_table = 'hall'

    def __str__(self):
        return self.name_hall


class Place(models.Model):
    name_place = models.CharField(max_length=255)

    class Meta:
        db_table = 'place'

    def __str__(self):
        return self.name_place


class HallPlace(models.Model):
    name_hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='hp_id_hall')
    name_place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='hp_id_place')

    class Meta:
        db_table = 'hall_place_location'

    def __str__(self):
        return f"{self.name_hall.name_hall} - {self.name_place.name_place}"


class HistoricalCulture(models.Model):
    name_cult = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name='hc_id_cult')
    name_hist = models.ForeignKey(Historical_period, on_delete=models.CASCADE, related_name='hc_id_hist')

    class Meta:
        db_table = 'historical_culture'

    def __str__(self):
        return f"{self.name_cult.name_cult} - {self.name_hist.name_hist}"

@deconstructible
class UploadToPathAndRename(object):
    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = os.path.splitext(filename)[1]
        filename = '{}{}'.format(instance.uniq_name, ext)
        return os.path.join(self.sub_path, filename)
class Artefact(models.Model):
    museum = models.ForeignKey(Museum, on_delete=models.CASCADE, related_name='id_museum')
    ex_monument = models.ForeignKey(Ex_monument, on_delete=models.CASCADE, related_name='id_ex_monument')
    year = models.ForeignKey(Year_monument, on_delete=models.CASCADE, related_name='id_year')
    uniq_name = models.CharField(max_length=255, unique=True)
    number = models.PositiveBigIntegerField(unique=True)
    name_art = models.CharField(max_length=255, null=True)
    material = models.ForeignKey(Material, blank=True, null=True, on_delete=models.CASCADE, related_name='id_material')
    histcult = models.ForeignKey(HistoricalCulture, blank=True, null=True, on_delete=models.CASCADE, related_name='id_hist_cult')
    age = models.CharField(max_length=30, blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    ex_lead = models.ForeignKey(Ex_lead, on_delete=models.CASCADE, related_name='id_lead_ex')
    location = models.ForeignKey(HallPlace, on_delete=models.CASCADE, related_name='id_hall_place')
    description = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to=UploadToPathAndRename('images/'))
    user_last_changes = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'artefact'
        get_latest_by = 'last_modified'

    def __str__(self):
        return str(self.id) +" | " + str(self.uniq_name)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # обновление существующего объекта
            old_obj = Artefact.objects.get(pk=self.pk)
            if old_obj.image.name != self.image.name:
                # Удаление старого файла
                if old_obj.image:
                    default_storage.delete(old_obj.image.name)

        # сохранение объекта, включая изменения в поле image
        super(Artefact, self).save(*args, **kwargs)
