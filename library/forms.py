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

class BookForm(forms.ModelForm):

    class Meta:
        content = forms.CharField(widget=forms.Textarea)
        model = Book
        fields = ('name_book','annotation','note','type')
        labels = {'name_book':'Название', 'annotation': 'Аннотация', 'note': 'Примечание', 'type': 'Тип'}
        widgets = {
            'name_book': forms.TextInput(attrs={'class': 'form-control'}),
            'annotation': Textarea(attrs={'class': 'form-control','cols': 15, 'rows': 10}),
            'note': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'})
        }

class BookAuthorForm(forms.ModelForm):

    class Meta:
        model = BookAuthor
        fields = ('author',)
        labels = {'author': 'Автор'}
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control'})
        }

class BookTagForm(forms.Form):
    tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=Select2MultipleWidget(attrs={"class": 'form-control',"onchange":"get_selected();"}),required=False)

class StorageForm(forms.ModelForm):

    class Meta:
        model = Storage
        fields = ('closet','shelf','link')
        labels = {'closet': 'Шкаф','shelf': 'Полка','link': 'Ссылка'}
        widgets = {
            'closet': forms.TextInput(attrs={'class': 'form-control'}),
            'shelf': forms.TextInput(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'class': 'form-control'}),
        }

class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = '__all__'


class TypeForm(forms.ModelForm):

    class Meta:
        model = Type
        fields = '__all__'

class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ('name',)
        labels = {'name': 'Автор'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

class CopyForm(forms.ModelForm):

    class Meta:
        model = Copy
        fields = ('year','part','release')
        labels = {'year': 'Год издания', 'part':'Часть', 'release': 'Выпуск'}
        widgets = {
            'year': forms.TextInput(attrs={'class': 'form-control'}),
            'part': forms.TextInput(attrs={'class': 'form-control'}),
            'release': forms.TextInput(attrs={'class': 'form-control'})
        }


