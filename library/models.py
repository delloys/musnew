from django.db import models
from django.conf import settings

# Create your models here.

class Tag(models.Model):
    tag = models.CharField(max_length=45)

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.tag

class Type(models.Model):
    type = models.CharField(max_length=45)

    class Meta:
        db_table = 'type'

    def __str__(self):
        return self.type

class Author(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'author'

    def __str__(self):
        return self.name

class Book(models.Model):
    name_book = models.TextField()
    annotation = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='id_type',blank=True, null=True)

    class Meta:
        db_table = 'book'

    def __str__(self):
        return self.name_book

class Storage(models.Model):
    closet = models.CharField(max_length=4, null=True, blank=True)
    shelf = models.CharField(max_length=4, blank=True, null=True)
    date_rec = models.DateTimeField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='id_type', blank=True, null=True)

    class Meta:
        db_table = 'storage'

    def __str__(self):
        return self.closet + " - " + str(self.shelf)

class BookAuthor(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='ba_id_author',blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ba_id_book')

    class Meta:
        db_table = 'book_author'

    def __str__(self):
        return str(self.author)

class BookTag(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bt_id_book')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='bt_id_tag', blank=True, null=True)

    class Meta:
        db_table = 'book_tag'

    def __str__(self):
        return str(self.id)

class Copy(models.Model):
    year = models.IntegerField(blank=True, null=True)
    part = models.CharField(max_length=20, blank=True, null=True)
    release = models.CharField(max_length=20, blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='copy_id_book')

    class Meta:
        db_table = 'copy'

    def __str__(self):
        return str(self.id)