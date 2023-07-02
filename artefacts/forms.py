from django import forms
from datetime import datetime
from .models import *
from django.forms import Textarea
from django.core.exceptions import ValidationError
from datetime import datetime
from django.forms.widgets import FileInput, ClearableFileInput

def validate_no_numbers(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('Поле не должно содержать цифры.')
class DescNoteTextarea(Textarea):
    def __init__(self, attrs=None):
        default_attrs = {'cols': 80, 'rows': 5}  # задаем размеры текстового поля
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

class ArtefactForm(forms.ModelForm):
    museum = forms.ModelChoiceField(queryset=Museum.objects.all(), required=False)
    material = forms.ModelChoiceField(queryset=Material.objects.all(), required=False)
    class Meta:
        model = Artefact
        fields = ('museum', 'ex_monument', 'year', 'uniq_name', 'number', 'name_art',
                  'material', 'histcult', 'age', 'size', 'ex_lead', 'location', 'description',
                  'note', 'image')
        labels = {
            'uniq_name': 'Уникальное название',
            'number': 'Номер артефакта',
            'name_art': 'Название артефакта',
            # и т.д.
        }
        widgets = {
                   'note': DescNoteTextarea(),
                   'description': DescNoteTextarea()
                   }


    def clean_uniq_name(self):
        """
        Проверка на уникальность значения поля `uniq_name`
        """
        uniq_name = self.cleaned_data.get('uniq_name')
        if Artefact.objects.filter(uniq_name=uniq_name).exists():
            raise forms.ValidationError('Уникальный шифр уже существует')
        return uniq_name

    def clean_number(self):
        """
        Проверка на уникальность значения поля `number`
        """
        number = self.cleaned_data.get('number')
        if Artefact.objects.filter(number=number).exists():
            raise forms.ValidationError('Уникальный номер уже существует')
        return number

class ArtefactEditForm(forms.ModelForm):
    class Meta:
        model = Artefact
        fields = ('museum', 'ex_monument', 'year', 'uniq_name', 'number', 'name_art', 'material', 'histcult', 'age', 'size', 'ex_lead', 'location', 'description', 'note', 'image')
        labels = {'uniq_name': 'Уникальное название', 'number': 'Номер артефакта', 'name_art': 'Название артефакта',
        }
        widgets = {'number': forms.TextInput(attrs={'readonly': 'readonly'}),
                   'uniq_name': forms.TextInput(attrs={'readonly': 'readonly'}),
                   'note': DescNoteTextarea(),
                   'description' : DescNoteTextarea(),
                   'image': ClearableFileInput(attrs={'clearable': True}),
         }
class MuseumForm(forms.ModelForm):
    class Meta:
        model = Museum
        fields = ['name_mus']
        labels = {
            'Museum': 'Музей',
            'name_mus': 'Название музея',
        }

    def clean_name_mus(self):
        """
        Проверка на уникальность значения поля `name_mus`
        """
        name_mus = self.cleaned_data.get('name_mus')
        if Museum.objects.filter(name_mus=name_mus).exists():
            raise forms.ValidationError('Такой музей уже существует')
        return name_mus

class MaterialForm(forms.ModelForm):
    name_mat = forms.CharField(label='Название материала', validators=[validate_no_numbers])
    class Meta:
        model = Material
        fields = ['name_mat']
        labels = {
            'name_mat': 'Название материала',
        }

    def clean_name_mat(self):
        """
        Проверка на уникальность значения поля `name_mat`
        """
        name_mat = self.cleaned_data.get('name_mat')
        if Material.objects.filter(name_mat=name_mat).exists():
            raise forms.ValidationError('Такой материал уже существует')
        return name_mat
class MonumentForm(forms.ModelForm):
    class Meta:
        model = Ex_monument
        fields = ['name_ex']
        labels = {
            'Ex_monument': 'Памятник',
            'name_ex': 'Название памятника',
        }

    def clean_name_ex(self):
        """
        Проверка на уникальность значения поля `name_ex`
        """
        name_ex = self.cleaned_data.get('name_ex')
        if Ex_monument.objects.filter(name_ex=name_ex).exists():
            raise forms.ValidationError('Такой памятник уже существует')
        return name_ex

class LeadForm(forms.ModelForm):
    name_ex_lead = forms.CharField(label='Руководитель раскопок',validators=[validate_no_numbers])
    class Meta:
        model = Ex_lead
        fields = ['name_ex_lead']
        labels = {
            'Ex_lead': 'Руководитель раскопок',
            'name_ex_lead': 'Руководитель раскопок',
        }

    def clean_name_ex_lead(self):
        """
        Проверка на уникальность значения поля `name_ex_lead`
        """
        name_ex_lead = self.cleaned_data.get('name_ex_lead')
        if Ex_lead.objects.filter(name_ex_lead=name_ex_lead).exists():
            raise forms.ValidationError('Такой руководитель уже существует в базе')
        return name_ex_lead

# class YearForm(forms.ModelForm):
#     class Meta:
#         model = Year_monument
#         fields = ['year']
#         labels = {
#             'year': 'Год раскопок',
#         }
#
#     def clean_year(self):
#         """
#         Проверка на уникальность значения поля `year`
#         и на то, что дата не больше текущей даты
#         """
#         year = self.cleaned_data.get('year')
#         if Year_monument.objects.filter(year=year).exists():
#             raise forms.ValidationError('Такой год уже есть в базе')

# class YearForm(forms.ModelForm):
#     year = forms.IntegerField(label='Год раскопок', required=False)
#
#     class Meta:
#         model = Year_monument
#         fields = ['year']
#         labels = {
#             'year': 'Год раскопок',
#         }
#
#     def clean_year(self):
#         year = self.cleaned_data.get('year')
#         if not year:
#             return None
#         if Year_monument.objects.filter(year=year).exists():
#             raise forms.ValidationError('Такой год уже есть в базе')
#         return year

class YearForm(forms.ModelForm):
    year = forms.IntegerField(label='Год раскопок', required=False)

    class Meta:
        model = Year_monument
        fields = ['year']
        labels = {
            'year': 'Год раскопок',
        }

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if not year:
            return None
        current_year = datetime.now().year
        if year > current_year:
            raise forms.ValidationError('Год не может быть больше текущего года')
        if Year_monument.objects.filter(year=year).exists():
            raise forms.ValidationError('Такой год уже есть в базе')
        return year
# class CultureForm(forms.ModelForm):
#     name_cult = forms.CharField(validators=[validate_no_numbers])
#
#     class Meta:
#         model = Culture
#         fields = ['name_cult']
#         labels = {
#             'name_cult': 'Культура',
#         }
#
#     def clean_name_cult(self):
#         """
#         Проверка на уникальность значения поля `name_cult`
#         """
#         name_cult = self.cleaned_data.get('name_cult')
#         if Culture.objects.filter(name_cult=name_cult).exists():
#             self.add_error('name_cult', 'Такая культура уже существует в базе')
#         return name_cult
#
#
# def validate_no_numbers(value):
#         if any(char.isdigit() for char in value):
#             raise ValidationError('Поле не должно содержать цифры.')

class CultureForm(forms.ModelForm):
    name_cult = forms.CharField(validators=[validate_no_numbers])

    class Meta:
        model = Culture
        fields = ['name_cult']
        labels = {
            'name_cult': 'Культура',
        }
    def clean_name_cult(self):
        """
        Проверка на уникальность значения поля `name_cult`
        """
        name_cult = self.cleaned_data.get('name_cult')
        if Culture.objects.filter(name_cult=name_cult).exists():
            self.add_error('name_cult', 'Такая культура уже существует в базе')
        return name_cult

# Форма для заполнения таблицы Historical_period
class HistoricalPeriodForm(forms.ModelForm):
    name_hist = forms.CharField(validators=[validate_no_numbers])

    class Meta:
        model = Historical_period
        fields = ['name_hist']
        labels = {
            'name_hist': 'Исторический период',
        }

    def clean_name_hist(self):
            """
            Проверка на уникальность значения поля `name_hist`
            """
            name_hist = self.cleaned_data.get('name_hist')
            if Historical_period.objects.filter(name_hist=name_hist).exists():
                raise forms.ValidationError('Такой исторический период уже существует в базе')
            return name_hist

# Форма для заполнения таблицы HistoricalCulture
class HistoricalCultureForm(forms.ModelForm):
    name_cult = forms.ModelChoiceField(queryset=Culture.objects.all(), required=False)
    name_hist = forms.ModelChoiceField(queryset=Historical_period.objects.all(), required=False)

    class Meta:
        model = HistoricalCulture
        fields = ['name_cult', 'name_hist']
        labels = {
            'name_hist': 'Исторический период',

    }

    def clean(self):
        cleaned_data = super().clean()
        name_cult = cleaned_data.get('name_cult')
        name_hist = cleaned_data.get('name_hist')

        if name_cult and name_hist:
            if HistoricalCulture.objects.filter(name_cult=name_cult, name_hist=name_hist).exists():
                raise forms.ValidationError('Такая связь между культурой и историческим периодом уже существует.')
        return cleaned_data

class HallForm(forms.ModelForm):
    name_hall = forms.CharField()

    class Meta:
        model = Hall
        fields = ['name_hall']
        labels = {
            'Hall': 'Зал',
            'name_hall': 'Зал',
        }

    def clean_name_hall(self):
            """
            Проверка на уникальность значения поля `name_hall`
            """
            name_hall = self.cleaned_data.get('name_hall')
            if Hall.objects.filter(name_hall=name_hall).exists():
                raise forms.ValidationError('Такой зал уже существует в базе')
            return name_hall

# Форма для заполнения таблицы Historical_period
class PlaceForm(forms.ModelForm):
    name_place = forms.CharField()

    class Meta:
        model = Place
        fields = ['name_place']
        labels = {
            'name_place': 'Место',
        }

    def clean_name_place(self):
            """
            Проверка на уникальность значения поля `name_place`
            """
            name_place = self.cleaned_data.get('name_place')
            if Place.objects.filter(name_place=name_place).exists():
                raise forms.ValidationError('Такое место уже существует в базе')
            return name_place

# Форма для заполнения таблицы HistoricalCulture
class HallPlaceForm(forms.ModelForm):
    name_hall = forms.ModelChoiceField(queryset=Hall.objects.all(), required=False)
    name_place = forms.ModelChoiceField(queryset=Place.objects.all(), required=False)

    class Meta:
        model = HallPlace
        fields = ['name_hall', 'name_place']
        labels = {
            'name_hall': 'Зал',
            'name_place': 'Место',
    }

    def clean(self):
        cleaned_data = super().clean()
        name_hall = cleaned_data.get('name_hall')
        name_place = cleaned_data.get('name_place')


        if name_place and name_hall:
            if HallPlace.objects.filter(name_place=name_place, name_hall=name_hall).exists():
                raise forms.ValidationError('Такая связь между залом и местом уже существует.')

        return cleaned_data