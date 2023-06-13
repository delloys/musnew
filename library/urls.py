from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.info_about_books), name='info_about_books'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('book/new', login_required(views.add_book),name='add_book'),
    path('book/<int:pk>/', login_required(views.detail_book), name='book_detail'),
    path('book/<int:pk>/edit/',login_required(views.edit_book), name='edit_book'),
    path('book/<int:pk>/delete/',login_required(views.delete_book), name='delete_book'),
    path('library/import/', login_required(views.upload_file), name='upload_file'),
    path('library/edit/', login_required(views.edit_additional_info), name='edit_additional_info'),
    path('author/<int:pk>/delete/',login_required(views.delete_author),name='delete_author'),
    path('type/<int:pk>/delete/',login_required(views.delete_type),name='delete_type'),
    path('tag/<int:pk>/delete/',login_required(views.delete_tag),name='delete_tag'),
    path('help/',login_required(views.help_render),name='help'),
]