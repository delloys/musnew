from django.shortcuts import render, redirect, get_object_or_404
import datetime
from django.http import HttpResponse,HttpResponseRedirect
import pandas as pd
import numpy as np
import math
from django.utils import timezone

from time import gmtime, strftime
from django.contrib import messages
from django.db import connection
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.forms import formset_factory,inlineformset_factory
from library.forms import *
from library.models import Book,BookTag,BookAuthor,Author,Tag,Type,Storage

from .forms import UploadFileForm
from dateutil.parser import parse

def help_render(request):
    return render(request,'library/help.html')

def edit_additional_info(request):
    if request.method == 'POST':
        author_edit = request.POST.get('authors')
        tag_edit = request.POST.get('tags')
        type_edit = request.POST.get('types')

        author_edit_data = AuthorForm(request.POST)
        tag_edit_data = TagForm(request.POST)
        type_edit_data = TypeNewForm(request.POST)

        if author_edit:
            get_author = Author.objects.get(name=author_edit)
            author_form = AuthorForm(initial={'name':get_author.name})
            check_author_form = True
            author_id = get_object_or_404(Author, name=author_edit)
        else:
            author_id = 1
            author_form = AuthorForm()
            check_author_form = False

        if tag_edit:
            get_tag = Tag.objects.get(tag=tag_edit)
            tag_form = TagForm(initial={'tag':get_tag.tag})
            check_tag_form = True
            tag_id = get_object_or_404(Tag, tag=tag_edit)
        else:
            tag_id = 1
            tag_form = TagForm()
            check_tag_form = False

        if type_edit:
            get_type = Type.objects.get(type=type_edit)
            type_form = TypeNewForm(initial={'type':get_type.type})
            check_type_form = True
            type_id = get_object_or_404(Type, type=type_edit)
        else:
            type_id = 1
            type_form = TypeNewForm()
            check_type_form = False
        post_check = True

        if author_edit_data.is_valid():
            formAuthor = AuthorForm(request.POST)
            save_author = formAuthor.save(commit=False)
            save_author.id = request.POST.get('id_author')
            save_author.save()
            messages.success(request, 'Автор успешно изменён.')
        if tag_edit_data.is_valid():
            formTag = TagForm(request.POST)
            save_tag = formTag.save(commit=False)
            save_tag.id = request.POST.get('id_tag')
            if save_tag.tag != request.POST.get('id_tag') and request.POST.get('id_tag') is not None :
                save_tag.save()
                messages.success(request, 'Тэг успешно изменён.')
        if type_edit_data.is_valid():
            save_type = type_edit_data.save(commit=False)
            save_type.id = request.POST.get('id_type')
            if save_type.type != request.POST.get('id_type') and request.POST.get('id_type') is not None:
                save_type.save()
                messages.success(request, 'Тип успешно изменён.')

        if request.POST.get('render_request'):
            return redirect('/')
    else:
        author_edit = AuthorEditForm()
        author_form = AuthorForm()
        tag_edit = TagEditForm()
        tag_form = TagForm()
        type_edit = TypeEditForm()
        type_form = TypeNewForm()
        check_author_form = False
        check_tag_form = False
        check_type_form = False
        post_check = False
        author_id = 1
        tag_id = 1
        type_id = 1
    return render(request,'library/edit_additional_info.html', {'author_edit_form': author_edit,'check_author_form':check_author_form,'author_form':author_form,
                                                                'tag_edit_form':tag_edit,'check_tag_form':check_tag_form,'tag_form':tag_form,
                                                                'post_check':post_check,
                                                                'type_edit_form':type_edit,'check_type_form':check_type_form,'type_form':type_form,
                                                                'author_id':author_id,'type_id':type_id,'tag_id':tag_id})

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def parse_file(filename):
  df1 = pd.read_excel(filename, sheet_name='Лист1')

  df1['Выпуск'] = "-"
  df1['Шкаф'] = "-"
  df1['Полка'] = "-"
  df1['Ссылка'] = "-"
  df1['Типы'] = "-"
  df1['Тэги'] = "-"
  df1.rename(columns={'возможна аннотация подумать':'Аннотация','ссылка на электронную версию книги':'Ссылка','Автор ':'Авторы','примечание':'Примечание','дата поступления':'Дата поступления'}, inplace = True)

  types = ['словарь','сборник','сборрник','препринт','периодическая литература','журнал','сборник статей','атлас','учебное пособие','каталог выставки','монография','путеводитель','метод. указания','тезисы докладов','отдельный оттиск','оттиск','справочник','путеводитель по выставке','методические рекомендации']
  df1 = df1.replace ( r'^\s\*$' , np.nan , regex= True )
  df1 = df1.fillna('-')

  #writer = pd.ExcelWriter('output.xlsx')

  for i in range(len(df1)):
    if "№" in str(df1['Год издания'][i]):
      str_part = df1.at[i,'Год издания'].replace(",","")
      str_part = str_part.partition(' ')
      for strs in str_part:
        if "№" in strs:
          df1.at[i,'Выпуск'] = strs
        elif strs != ' ':
          df1.at[i,'Год издания'] = strs
    if "том" in str(df1['Год издания'][i]).lower():
      str_part = df1.at[i,'Год издания'].replace(",","")
      str_part = str_part.partition(' ')
      for strs in str_part:
        if "том" in strs:
          df1.at[i,'Выпуск'] = strs
        elif strs != ' ':
          df1.at[i,'Год издания'] = strs
    if "выпуск" in str(df1['Год издания'][i]).lower():
      str_part = df1.at[i,'Год издания'].replace(",","")
      str_part = str_part.partition(' ')
      for strs in str_part:
        if "выпуск" in strs:
          df1.at[i,'Выпуск'] = strs
        elif strs != ' ':
          df1.at[i,'Год издания'] = strs
    if "вып." in str(df1['Год издания'][i]).lower():
      str_part = df1.at[i,'Год издания'].replace(",","")
      str_part = str_part.partition(' ')
      for strs in str_part:
        if "вып." in strs:
          df1.at[i,'Выпуск'] = strs
        elif strs != ' ':
          df1.at[i,'Год издания'] = strs
    if ("-" in str(df1['Год издания'][i])) and len(str(df1['Год издания'][i])) != 1:
        df1.at[i,'Примечание'] = df1['Год издания'][i]
        df1.at[i,'Год издания'] = df1['Год издания'][i][:4]
    if ", " in str(df1['Год издания'][i]):
      str_part = df1.at[i,'Год издания'].replace(",","")
      str_part = str_part.partition(' ')
      for strs in str_part:
        if strs != ' ' and strs.isnumeric():
          if (1500 < int(strs) < 2200):
            df1.at[i,'Год издания'] = strs
          else:
            df1.at[i,'Выпуск'] = strs
        elif strs != ' ':
            df1.at[i,'Выпуск'] = strs

    if str(df1['Год издания'][i]).lower() == 'н/у' or str(df1['Год издания'][i]) == '':
      df1.at[i,'Год издания'] = '-'

    if str(df1['Авторы'][i]).lstrip().rstrip().lower() in types:
      df1.at[i,'Типы'] = df1['Авторы'][i]
      df1.at[i,'Авторы'] = '-'
    if str(df1['Авторы'][i]) == 'Н/у' or str(df1['Авторы'][i]) == '':
      df1.at[i,'Авторы'] = '-'

    if "шк" in str(df1['Место хранения'][i]).lower():
      str_part = df1.at[i,'Место хранения'].replace("Шк","")
      str_part = str_part.replace('П ','')
      str_part = str_part.replace(', п','')
      str_part = str_part.replace(' ','')
      str_part = str_part.replace('..','.')
      str_part = str_part[1:]
      str_part = str_part.partition('.')
      df1.at[i,'Шкаф'] = str_part[0]
      df1.at[i,'Полка'] = str_part[2]
    if "шкаф" in str(df1['Место хранения'][i]).lower():
      str_part = df1.at[i,'Место хранения'].replace("шкаф","")
      str_part = str_part.replace('полка','')
      str_part = str_part.replace(' ','')
      str_part = str_part.partition(',')
      df1.at[i,'Шкаф'] = str_part[0]
      df1.at[i,'Полка'] = str_part[2]

  df1 = df1.drop(['Место хранения', 'Ссылка'], axis='columns')
  #df1.to_excel(writer) # save the excel
  #writer.save()

  return df1

def handle_uploaded_file(f):
    with open("library/media/name.txt", "wb+") as destination:
        if type(f) == str:
            destination.write(f.encode())  # or whatever you actually want to do if it's a string
        else:
            for chunk in f.chunks():
                destination.write(chunk)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            for filename, file in request.FILES.items():
                name = request.FILES[filename].name
            #if not handle_uploaded_file(name):
                form.save()
                files = ExcelImport.objects.latest('id')
                #print(files.id,'YTYTY')
                #print(f.file_excel.name,'popoperop',len(files))
                #to pythonanywhere use
                books_df = parse_file('dvfumuseum.pythonanywhere.com/library/media/' + files.file_excel.name)
                #to local
                #books_df = parse_file('library/media/' + files.file_excel.name)
                for i in range(len(books_df)):
                    book_Model = Book()
                    book_Model.name_book = books_df.at[i,'Название']
                    book_Model.annotation = books_df.at[i,'Аннотация']
                    book_Model.note = books_df.at[i,'Примечание']
                    if books_df.at[i,'Типы'] != '-':
                        get_type, created = Type.objects.get_or_create(type=books_df.at[i,'Типы'].rstrip().lstrip())
                        book_Model.type = get_type
                    book_Model.save()
                    book_Storage = Storage()
                    book_Storage.book_id = book_Model.id
                    book_Storage.closet = books_df.at[i,'Шкаф']
                    book_Storage.shelf = books_df.at[i,'Полка']
                    book_Storage.user_id = request.user.id
                    book_Storage.save()
                    book_Copy = Copy()
                    if "-" not in str(books_df.at[i,'Год издания']):
                        book_Copy.year = books_df.at[i,'Год издания']
                    if is_date(str(books_df.at[i,'Дата поступления'])):
                        book_Copy.receipt_date = books_df.at[i,'Дата поступления']
                    book_Copy.part = books_df.at[i,'Выпуск']
                    book_Copy.book_id = book_Model.id
                    book_Copy.save()
                    if str(books_df.at[i, 'Авторы']) != 'nan' and str(books_df.at[i, 'Авторы']) != '' and str(books_df.at[i, 'Авторы']) != '-':
                        authors_list = books_df.at[i, 'Авторы'].replace(' и ', ',').split(',')
                        for i in range(len(authors_list)):
                            authors_list[i] = authors_list[i].rstrip().lstrip()
                            get_author, created = Author.objects.get_or_create(name=authors_list[i])
                            book_BookAuthor = BookAuthor()
                            book_BookAuthor.author_id = get_author.id
                            book_BookAuthor.book_id = book_Model.id
                            book_BookAuthor.save()
                ExcelImport.objects.latest('id').delete()
                messages.success(request, 'Данные успешно добавлены.')
                return redirect('/')
    else:
        form = UploadFileForm()

    return render(request, 'library/upload.html', {'form': form})

def delete_type(request,pk):
    Type.objects.filter(pk=pk).delete()
    messages.success(request, 'Тип успешно удален.')
    return redirect('/')

def delete_tag(request,pk):
    Tag.objects.filter(pk=pk).delete()
    messages.success(request, 'Тэг успешно удален.')
    return redirect('/')

def delete_author(request,pk):
    Author.objects.filter(pk=pk).delete()
    messages.success(request, 'Автор успешно удален.')
    return redirect('/')

def delete_book(request,pk):
    Book.objects.filter(pk=pk).delete()
    messages.success(request, 'Книга успешно удалена.')
    return redirect('/')

def create_empty_storage(request,book):
    storage = Storage()
    storage.shelf = ''
    storage.closet = ''
    storage.link = ''
    storage.user_id = request.user.id
    storage.book_id = book.id
    storage.save()
    storage = Storage.objects.filter(book=book.id)

    return storage

def create_empty_copy(book):
    copy = Copy()
    copy.year = ''
    copy.part = ''
    copy.release = ''
    copy.book_id = book.id
    copy.save()
    copy = Copy.objects.filter(book=book.id)

    return copy
def get_book_detail(pk):
    with connection.cursor() as cursor:
        cursor.execute('''
            WITH get_authors(ID_Book,ID_Author, authors_name)
            AS (SELECT book_id,GROUP_CONCAT(author_id),GROUP_CONCAT(name) 
                FROM author 
                LEFT JOIN book_author ON author.id=book_author.author_id 
                GROUP BY book_id),
             get_tag(ID_Book, ID_Tag, tag_book)
            AS(SELECT book_id,GROUP_CONCAT(tag_id),GROUP_CONCAT(tag) 
                    FROM book_tag 
                    LEFT JOIN tag ON book_tag.tag_id=tag.id
	            GROUP BY book_id),
             get_storage(ID_Storage,ID_Book,ID_User,link,mesto,last_modified_time)
            AS(SELECT id,book_id,user_id,link, CONCAT_WS(" ",closet,shelf),last_modified_time FROM storage)
        
            SELECT book.id AS 'Номер',
            IFNULL(authors_name,'-') AS 'Авторы',
            name_book AS 'Название',
            IFNULL(part,'-') AS 'Том',
            IFNULL(year,'-') AS 'Год Издания',
            last_modified_time AS 'Последние изменения',
            IFNULL(tag_book,'-') AS 'Тэг',
            IFNULL(type,'-') AS 'Тип',
            IFNULL(annotation,'-') AS 'Аннотация',
            IFNULL(note,'-') AS 'Заметки',
            IFNULL(mesto,'-') AS 'Расположение',
            IFNULL(link,'-') AS 'Ссылка',
            receipt_date AS 'Дата поступления',
            first_name,
            last_name
            FROM book
                LEFT JOIN type ON book.type_id=type.id
                LEFT JOIN get_authors ON book.id=get_authors.ID_Book
                LEFT JOIN get_tag ON book.id=get_tag.ID_Book
                LEFT JOIN copy ON book.id=copy.book_id
                LEFT JOIN get_storage ON book.id=get_storage.ID_Book
                LEFT JOIN auth_user ON get_storage.ID_User=auth_user.id
            WHERE (book.id = %s); 
            ''',(pk,))
        row = cursor.fetchone()
    return row

def edit_book(request, pk):
    update_book = get_object_or_404(Book, pk=pk)
    authors = Author.objects.filter(ba_id_author__book=update_book.id)
    tags = Tag.objects.filter(bt_id_tag__book=update_book.id)
    title = update_book.name_book

    if Storage.objects.filter(book=update_book.id).exists():
        stor = Storage.objects.filter(book=update_book.id)
    else:
        stor = create_empty_storage(request,update_book)
    if Copy.objects.filter(book=update_book.id).exists():
        copy = Copy.objects.filter(book=update_book.id)
    else:
        copy = create_empty_copy(update_book)

    if request.method == 'POST':
        tag = request.POST.get('tags')
        author = request.POST.get('authors')
        types = request.POST.get('types')
        formBook = BookForm(request.POST)
        formCopy = CopyForm(request.POST)
        formStorage = StorageForm(request.POST)
        formAuthor = AuthorBookForm(request.POST)

        print(tag,'TAGS',len(tags),types)

        if formBook.is_valid():
            book = formBook.save(commit=False)
            update_book.name_book = book.name_book
            update_book.annotation = book.annotation
            update_book.note = book.note
            if types is not None:
                types = types[1:].rstrip().lstrip()
                type_get, created = Type.objects.get_or_create(type=types)
                update_book.type = type_get
            update_book.save()
        if tag is not None:
            bookTag = BookTag.objects.filter(book_id=update_book.id)
            for i in range(len(bookTag)):
                bookTag[i].delete()
            splitTags = tag[1:].split(';')
            for i in range(len(splitTags)):
                tag_get, created = Tag.objects.get_or_create(tag=splitTags[i].rstrip().lstrip())
                print(tag_get)
                set_bookTag = BookTag()
                set_bookTag.book_id = update_book.id
                set_bookTag.tag_id = tag_get.id
                set_bookTag.save()
                print(set_bookTag,'SETBOKTAG')
        if author is not None:
            bookAuthor = BookAuthor.objects.filter(book_id=update_book.id)
            if author == 'undefined':
                for i in range(len(bookAuthor)):
                    print(bookAuthor[i],'FGFG')
                    bookAuthor[i].delete()
            else:
                for i in range(len(bookAuthor)):
                    bookAuthor[i].delete()
                splitAuthors = author[1:].split(';')
                for i in range(len(splitAuthors)):
                    author_get, created = Author.objects.get_or_create(name=splitAuthors[i].rstrip().lstrip())
                    set_bookAuthor = BookAuthor()
                    set_bookAuthor.book_id = update_book.id
                    set_bookAuthor.author_id = author_get.id
                    set_bookAuthor.save()
        if formCopy.is_valid():
            bookCopy = Copy.objects.filter(book_id=update_book.id)
            for i in range(len(bookCopy)):
                bookCopy[i].delete()
            copy = formCopy.save(commit=False)
            copy.book_id = update_book.id
            copy.save()
            print(copy.receipt_date,'TRTRR')
        if formStorage.is_valid():
            bookStorage = Storage.objects.get(book_id=update_book.id)
            bookStorage.delete()
            storage = formStorage.save(commit=False)
            storage.book_id = update_book.id
            storage.user_id = request.user.id
            storage.closet = bookStorage.closet
            storage.shelf = bookStorage.shelf
            storage.link = bookStorage.link
            storage.save()
        messages.success(request, 'Книга успешно изменена.')
        return redirect('/')
    else:
        print(type(copy[0].receipt_date),str(copy[0].receipt_date))
        formBook = BookForm(initial={'name_book': update_book.name_book,'annotation':update_book.annotation,'note':update_book.note})
        formAuthor = AuthorBookForm(initial={'author':authors})
        formCopy = CopyForm(initial={'year':copy[0].year,'part':copy[0].part,'release':copy[0].release,'receipt_date':str(copy[0].receipt_date)})
        formType = TypeForm(initial={'type':update_book.type})
        formStorage = StorageForm(initial={'closet':stor[0].closet,'shelf':stor[0].shelf,'link':stor[0].link})
        formBookTag = BookTagForm(initial={'tag':tags})
    return render(request, 'library/edit_book.html',{'formBook': formBook,'formAuthor': formAuthor,'formCopy':formCopy,'formStorage':formStorage, 'formBookTag': formBookTag,'formType':formType,'title':title})

#Информация об одной книге
def detail_book(request,pk):
    #book = get_object_or_404(Book, pk=pk)
    book = get_book_detail(pk)
    return render(request, 'library/book_detail.html', {'book': book})

#Добавление книги
def add_book(request):
    if request.method == 'POST':
        tag = request.POST.get('tags')
        author = request.POST.get('authors')
        types = request.POST.get('types')
        formBook = BookForm(request.POST)
        formCopy = CopyForm(request.POST)
        formStorage = StorageForm(request.POST)
        if formBook.is_valid():
            book = formBook.save(commit=False)
            book.save()

            set_tag = get_object_or_404(Book,pk=book.id)
            if types is not None:
                types = types[1:].rstrip().lstrip()
                type_get, created = Type.objects.get_or_create(type=types)
                set_tag.type = type_get
                set_tag.save()
            if author is not None:
                splitAuthors = author[1:].split(';')
                for i in range(len(splitAuthors)):
                    splitAuthors[i] = splitAuthors[i].rstrip().lstrip()
                    author_get, created = Author.objects.get_or_create(name=splitAuthors[i])
                    set_bookAuthor = BookAuthor()
                    set_bookAuthor.book_id = book.id
                    set_bookAuthor.author_id = author_get.id
                    set_bookAuthor.save()
            if formCopy.is_valid():
                copy = formCopy.save(commit=False)
                copy.book_id = book.id
                copy.save()
            else:
                messages.warning(request, 'Некорректные данные в одном из следующих полей: Год издания, Часть, Выпуск или Дата поступления. Пожалуйста, проверьте правильность данных.')
            if formStorage.is_valid():
                storage = formStorage.save(commit=False)
                storage.user_id = request.user.id
                storage.book_id = book.id
                storage.save()
                print(storage.last_modified_time)
            else:
                messages.warning(request,'Некорректные данные в одном из следующих полей: Шкаф, Полка, Ссылка. Пожалуйста, проверьте правильность данных.')
            if tag is not None:
                splitTags = tag[1:].split(';')
                for i in range(len(splitTags)):
                    splitTags[i] = splitTags[i].rstrip().lstrip()
                    tag_get, created = Tag.objects.get_or_create(tag=splitTags[i])
                    set_bookTag = BookTag()
                    set_bookTag.book_id = book.id
                    set_bookTag.tag_id = tag_get.id
                    set_bookTag.save()
            messages.success(request, 'Новая книга успешно добавлена')
        else:
            messages.success(request, 'Книга не добавлена.')
        return redirect('/')
    else:
        formBook = BookForm()
        formAuthor = AuthorBookForm()
        formCopy = CopyForm()
        formType = TypeForm()
        formStorage = StorageForm()
        formBookTag = BookTagForm()
    return render(request, 'library/add_book.html', {'formBook': formBook,'formAuthor': formAuthor,'formCopy':formCopy,'formStorage':formStorage, 'formBookTag': formBookTag,'formType':formType})

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
        IFNULL(authors_name,'-') AS 'Авторы',
        name_book AS 'Название',
        IFNULL(part,'-') AS 'Том',
        IFNULL(year,'-') AS 'Год Издания',
        IFNULL(tag_book,'-') AS 'Тэг',
        IFNULL(type,'-') AS 'Тип'
        FROM book
            LEFT JOIN type ON book.type_id=type.id
            LEFT JOIN get_authors ON book.id=get_authors.ID_Book
            LEFT JOIN get_tag ON book.id=get_tag.ID_Book
            LEFT JOIN copy ON book.id=copy.book_id
        ORDER BY book.id;
        ''')
        rows = cursor.fetchall()
    return rows

#Сгурппированные тэги для каждой книги
def grouped_tags_for_book():
    with connection.cursor() as cursor:
        cursor.execute('SELECT GROUP_CONCAT(tag_id), GROUP_CONCAT(tag), book_id FROM book_tag LEFT JOIN tag ON tag.id = book_tag.tag_id GROUP BY book_id;')
        row = cursor.fetchall()
    return row

def info_about_books(request):
    all_books = all_info_about_books()

    return render(request, 'library/info_about_books.html', {'all_books': all_books})