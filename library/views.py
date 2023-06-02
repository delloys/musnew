from django.shortcuts import render, redirect, get_object_or_404
import datetime
from django.http import HttpResponse,HttpResponseRedirect
from time import gmtime, strftime
from django.contrib import messages
from django.db import connection
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.forms import formset_factory,inlineformset_factory
from library.forms import *
from library.models import Book,BookTag,BookAuthor,Author,Tag,Type,Storage


def add_tag(request):
    if request.method == "POST":
        formTag = TagForm(request.POST)
        if formTag.is_valid():
            formTag.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        formTag = TagForm()
    return render(request, 'library/add_tag.html', {'formTag': formTag})

def get_book_detail(pk):
    with connection.cursor() as cursor:
        cursor.execute('''
            WITH get_authors(ID_Book,ID_Author, authors_name)
            AS (SELECT book_id,GROUP_CONCAT(author_id),GROUP_CONCAT(name) 
                FROM author 
                LEFT JOIN book_author ON author.id=book_author.author_id 
                GROUP BY book_id),
             get_tag(ID_Book, ID_Tag, tag_book)
            AS(SELECT book_id,tag_id,tag 
                   FROM book_tag 
                LEFT JOIN tag ON book_tag.tag_id=tag.id),
             get_storage(ID_Storage,ID_Book,link,mesto)
            AS(SELECT id,book_id,link, CONCAT_WS(" ",closet,shelf) FROM storage)
        
            SELECT book.id AS 'Номер',
            authors_name AS 'Авторы',
            name_book AS 'Название',
            part AS 'Том',
            year AS 'Год Издания',
            ID_Tag AS 'Тэг',
            type AS 'Тип',
            annotation AS 'Аннотация',
            note AS 'Заметки',
            mesto AS 'Расположение',
            link AS 'Ссылка'
            FROM book
                LEFT JOIN type ON book.type_id=type.id
                LEFT JOIN get_authors ON book.id=get_authors.ID_Book
                LEFT JOIN get_tag ON book.id=get_tag.ID_Book
                LEFT JOIN copy ON book.id=copy.book_id
                LEFT JOIN get_storage ON book.id=get_storage.ID_Book
            WHERE (book.id = %s); 
            ''',(pk,))
        row = cursor.fetchone()
    return row

#Информация об одной книге
def detail_book(request,pk):
    #book = get_object_or_404(Book, pk=pk)
    book = get_book_detail(pk)
    print(book[0])
    return render(request, 'library/book_detail.html', {'book': book})

#Добавление книги
def add_book(request):
    if request.method == 'POST':
        formBook = BookForm(request.POST)
        formAuthor = AuthorForm(request.POST)
        formBookAuthor = BookAuthorForm()
        formCopy = CopyForm(request.POST)
        formStorage = StorageForm(request.POST)
        formBookTag = BookTagForm(request.POST)
        if formBook.is_valid():
            book = formBook.save()
            if formAuthor.is_valid():
                author = formAuthor.save(commit = False)
                splitAuthors = author.name.split(sep=',')
                if len(splitAuthors) >= 1:
                    for i in range(len(splitAuthors)):
                        author_get, created = Author.objects.get_or_create(name=splitAuthors[i].lstrip())
                        set_bookAuthor = BookAuthor()
                        set_bookAuthor.author_id = author_get.id
                        set_bookAuthor.book_id = book.id
                        set_bookAuthor.save()
                else:
                    author.save()
                    bookAuthor = formBookAuthor.save(commit = False)
                    bookAuthor.author_id = author.id
                    bookAuthor.book_id = book.id
                    bookAuthor.save()
            if formCopy.is_valid():
                copy = formCopy.save(commit=False)
                copy.book_id = book.id
                copy.save()
            print('AAAAAAAAAAA',formStorage.is_valid() )
            if formStorage.is_valid():
                storage = formStorage.save(commit=False)
                storage.user_id = request.user.id
                storage.book_id = book.id
                storage.date_rec = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                storage.save()
            if formBookTag.is_valid():
                formBookTag = formBookTag.save(commit = False)
                print(formBookTag.tag,'boktag')
                formBookTag.book_id = book.id
                formBookTag.save()
        return redirect('/')
    else:
        formBook = BookForm()
        formAuthor = AuthorForm()
        formCopy = CopyForm()
        formStorage = StorageForm()
        formBookTag = BookTagForm()
    return render(request, 'library/add_book.html', {'formBook': formBook,'formAuthor': formAuthor,'formCopy':formCopy,'formStorage':formStorage, 'formBookTag': formBookTag})

#Информация о всех книгах в БД
def all_info_about_books():
    with connection.cursor() as cursor:
        cursor.execute('''
        WITH get_authors(ID_Book, authors_name)
         AS (SELECT book_id, GROUP_CONCAT(name)
             FROM author
                      LEFT JOIN book_author ON author.id=book_author.author_id
             GROUP BY book_id),
        get_tag(ID_Book, tag_book)
         AS (SELECT book_id, GROUP_CONCAT(tag)
 	     FROM book_tag 
			LEFT JOIN tag ON tag.id = book_tag.tag_id
	     GROUP BY book_id)
	     
	     SELECT book.id AS Номер,
        authors_name AS 'Авторы',
        name_book AS 'Название',
        part AS 'Том',
        year AS 'Год Издания',
        tag_book AS 'Тэг',
        type AS 'Тип'
        FROM book
            LEFT JOIN type ON book.type_id=type.id
            LEFT JOIN get_authors ON book.id=get_authors.ID_Book
            LEFT JOIN get_tag ON book.id=get_tag.ID_Book
            LEFT JOIN copy ON book.id=copy.book_id
        ORDER BY book.id;
        ''')
        row = cursor.fetchall()
    return row

#Сгурппированные тэги для каждой книги
def grouped_tags_for_book():
    with connection.cursor() as cursor:
        cursor.execute('SELECT GROUP_CONCAT(tag_id), GROUP_CONCAT(tag), book_id FROM book_tag LEFT JOIN tag ON tag.id = book_tag.tag_id GROUP BY book_id;')
        row = cursor.fetchall()
    return row

def info_about_books(request):
    all_books = all_info_about_books()
    print(all_info_about_books())
    return render(request, 'library/info_about_books.html', {'all_books': all_books})