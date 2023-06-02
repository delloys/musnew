from django.contrib import admin
from .models import *

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookTag)
admin.site.register(BookAuthor)
admin.site.register(Tag)
admin.site.register(Copy)
admin.site.register(Type)
admin.site.register(Storage)

