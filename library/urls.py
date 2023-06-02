from django.urls import path
from . import views

urlpatterns = [
    path('', views.info_about_books, name='info_about_books'),
    path('book/new', views.add_book,name='add_book'),
    path('book/<int:pk>/', views.detail_book, name='book_detail'),
    path('library/tag/add/',views.add_tag, name='add_tag')
]