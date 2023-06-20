from django.forms import inlineformset_factory, formset_factory
from django.forms.models import BaseInlineFormSet
from django import forms
from django.contrib.admin import site, widgets
from django.contrib import admin
from django.core.exceptions import ValidationError

from django_select2.forms import Select2Widget, Select2MultipleWidget
from django.forms import ModelForm, Textarea,CheckboxSelectMultiple,RadioSelect,ModelMultipleChoiceField
from library.models import *
from django.forms import formset_factory,inlineformset_factory

#BookFormset = inlineformset_factory(Book,BookAuthor,fields = '__all__')

class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields ={'name',}
        labels = {'name': 'Автор'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = {'tag',}
        labels = {'tag': 'Тэг'}
        widgets = {
            'tag': forms.TextInput(attrs={'class': 'form-control'})
        }

class TypeNewForm(forms.ModelForm):

    class Meta:
        model = Type
        fields = {'type',}
        labels = {'type':'Тип'}
        widgets = {
            'type': forms.TextInput(attrs={'class': 'form-control'})
        }
class BookForm(forms.ModelForm):

    class Meta:
        content = forms.CharField(widget=forms.Textarea)

        model = Book
        fields = ('name_book','annotation','note')
        labels = {'name_book':'Название', 'annotation': 'Аннотация', 'note': 'Примечание'}
        widgets = {
            'name_book': forms.TextInput(attrs={'class': 'form-control'}),
            'annotation': Textarea(attrs={'class': 'form-control','cols': 15, 'rows': 10}),
            'note': forms.TextInput(attrs={'class': 'form-control'}),

        }


class TypeForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('type',)
        labels = {'type':'Тип'}
        widgets = {
            'type': Select2Widget(attrs={"class": 'form-control',"onchange":"get_selected('type_div','type_requested','types','select2-selection__rendered');"})
        }
class BookTagForm(forms.Form):
    tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=Select2MultipleWidget(attrs={"class": 'form-control',"onchange":"get_selected('tag_div','tags_requested','tags','select2-selection__choice__display');"}),required=False,label='Тэг')

class AuthorBookForm(forms.Form):
    author = forms.ModelMultipleChoiceField(queryset=Author.objects.all(), widget=Select2MultipleWidget(attrs={"class": 'form-control',"onchange":"get_selected('author_div','author_requested','authors','select2-selection__choice__display');"}),required=False,label='Автор')

class AuthorEditForm(forms.Form):
    author = forms.ModelChoiceField(queryset=Author.objects.all(),widget=Select2Widget(attrs={"class": 'form-control',"onchange":"get_selected('author_div','author_requested','authors','select2-selection__rendered','author_form');"}),label='Автор')

class TagEditForm(forms.Form):
    tag = forms.ModelChoiceField(queryset=Tag.objects.all(),widget=Select2Widget(attrs={"class": 'form-control',"onchange":"get_selected('tag_div','tag_requested','tags','select2-selection__rendered','tag_form');"}),label='Тэг')

class TypeEditForm(forms.Form):
    type = forms.ModelChoiceField(queryset=Type.objects.all(),widget=Select2Widget(attrs={"class": 'form-control',"onchange":"get_selected('type_div','type_requested','types','select2-selection__rendered','type_form');"}),label='Тип')

class UploadFileForm(forms.ModelForm):

    class Meta:
        model = ExcelImport
        fields = ('file_excel',)
        labels = {'file_excel': 'Файл'}

class StorageForm(forms.ModelForm):

    class Meta:
        model = Storage
        fields = ('closet','shelf','link')
        labels = {'closet': 'Шкаф','shelf': 'Полка','link': 'Ссылка'}
        widgets = {
            'closet': forms.TextInput(attrs={'class': 'form-control'}),
            'shelf': forms.TextInput(attrs={'class': 'form-control'}),
            'link': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CopyForm(forms.ModelForm):

    class Meta:
        model = Copy
        fields = ('year','part','release','receipt_date')
        labels = {'year': 'Год издания', 'part':'Часть', 'release': 'Выпуск','receipt_date':'Дата поступления'}
        widgets = {
            'year': forms.TextInput(attrs={'class': 'form-control'}),
            'part': forms.TextInput(attrs={'class': 'form-control'}),
            'release': forms.TextInput(attrs={'class': 'form-control'}),
            'receipt_date':forms.DateInput(attrs={'class': 'form-control','type':'date'})
        }


