from django.shortcuts import render, get_object_or_404
from .forms import *
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from datetime import datetime
from .models import *


def add_new_info(request):
    return render(request,'artefacts/add_new_info.html')

def info_about_arts(request):
    artefacts = Artefact.objects.all()

    # Фильтрация поискового запроса
    search_query = request.GET.get('ex_monument', '')
    uniq_query = request.GET.get('uniq_name','')
    name_query = request.GET.get('name', '')
    museum_query = request.GET.get('museum', '')
    year_query = request.GET.get('year', '')
    lead_query = request.GET.get('ex_lead', '')

    if search_query or name_query or museum_query or year_query or uniq_query or lead_query:
        q = Q()
        if search_query:
            q |= Q(ex_monument__name_ex__icontains=search_query)
        if uniq_query:
            q &= Q(uniq_name__icontains=uniq_query)
        if name_query:
            q &= Q(name_art__icontains=name_query)
        if museum_query:
            q &= Q(museum__name_mus__icontains=museum_query)
        if year_query:
            q &= Q(year__year__icontains=year_query)
        if lead_query:
            q &= Q(ex_lead__name_ex_lead__icontains=lead_query)
        artefacts = artefacts.filter(q)

    # Сортировка
    sort_param = request.GET.get('sort', 'id')
    if sort_param:
        artefacts = artefacts.order_by(sort_param)

    return render(request, 'artefacts/info_about_arts.html', {'artefacts': artefacts, 'search_query': search_query})

def artefact_detail(request, pk):
    artefact = get_object_or_404(Artefact, pk=pk)
    return render(request, 'artefacts/artefact_detail.html', {'artefact': artefact})

def delete_artefact(request, pk):
    artefact = get_object_or_404(Artefact, pk=pk)
    artefact.delete()
    return redirect('info_about_arts')
def edit_artefact(request, pk):
    artefact = get_object_or_404(Artefact, pk=pk)
    if request.method == 'POST':
        form = ArtefactEditForm(request.POST, request.FILES, instance=artefact)
        if form.is_valid():
            artefact = form.save(commit=False)
            artefact.user_last_changes = request.user
            print(form.errors)
            artefact.save()
            form.save_m2m()
            messages.success(request, 'Артефакт успешно обновлен!')
            return redirect('artefact_detail', pk=artefact.pk)
    else:
        form = ArtefactEditForm(instance=artefact)
    return render(request, 'artefacts/edit_artefact.html', {'form': form, 'artefact': artefact})
def add_museum(request):
    context = "Добавить музей"
    if request.method == 'POST':
        form = MuseumForm(request.POST)
        if form.is_valid():
            museum = form.save()
            messages.success(request, 'Новый музей успешно добавлен!')
            # url = reverse('add_artefact') + '?museum={}'.format(museum.pk)
            url = reverse('add_museum')
            return redirect(url)
    else:
        museum_id = request.GET.get('museum')
        initial = {'name_mus': ''}
        if museum_id:
            museum = Museum.objects.get(pk=museum_id)
            initial['name_mus'] = museum.name_mus
        form = MuseumForm(initial=initial)
    return render(request, 'artefacts/add_list_with_context.html',{'form': form, 'context': context})

def add_material(request):
    context = "Добавить материал"
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save()
            messages.success(request, 'Новый материал успешно добавлен!')
            # url = reverse('add_artefact') + '?material={}'.format(material.pk)
            url = reverse('add_material')
            return redirect(url)
    else:
        material_id = request.GET.get('material')
        initial = {'name_mat': ''}
        if material_id:
            material = Material.objects.get(pk=material_id)
            initial['name_mat'] = material.name_mat
        form = MaterialForm(initial=initial)
    return render(request, 'artefacts/add_list_with_context.html',{'form': form, 'context': context})

def add_ex_monument(request):
    context = "Добавить памятник"
    if request.method == 'POST':
        form = MonumentForm(request.POST)
        if form.is_valid():
            monument = form.save()
            messages.success(request, 'Новый памятник успешно добавлен!')
            # url = reverse('add_artefact') + '?monument={}'.format(monument.pk)
            url = reverse('add_ex_monument')
            return redirect(url)
    else:
        monument_id = request.GET.get('monument')
        initial = {'name_ex': ''}
        if monument_id:
            monument = Ex_monument.objects.get(pk=monument_id)
            initial['name_ex'] = monument.name_ex
        form = MonumentForm(initial=initial)
    return render(request, 'artefacts/add_list_with_context.html',{'form': form, 'context': context})

def add_ex_lead(request):
    context = "Добавить руководителя"
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()
            messages.success(request, 'Новый руководитель успешно добавлен!')
            # url = reverse('add_artefact') + '?lead={}'.format(lead.pk)
            url = reverse('add_ex_lead')
            return redirect(url)
    else:
        lead_id = request.GET.get('lead')
        initial = {'name_ex_lead': ''}
        if lead_id:
            lead = Ex_lead.objects.get(pk=lead_id)
            initial['name_ex_lead'] = lead.name_ex_lead
        form = LeadForm(initial=initial)
    return render(request, 'artefacts/add_list_with_context.html',{'form': form, 'context': context})

def add_year(request):
    context = "Добавить новый год раскопок"
    if request.method == 'POST':
        form = YearForm(request.POST)
        if form.is_valid():
            year = form.save()
            messages.success(request, 'Новый год раскопок успешно добавлен!')
            # url = reverse('add_artefact') + '?year={}'.format(year.pk)
            url = reverse('add_year')
            return redirect(url)
    else:
        year_id = request.GET.get('year')
        initial = {'year': ''}
        if year_id:
            year = Year_monument.objects.get(pk=year_id)
            initial['year'] = year.year
        form = YearForm(initial=initial)
    return render(request, 'artefacts/add_list_with_context.html',{'form': form, 'context': context})

# def add_artefact(request):
#     if request.method == 'POST':
#         form = ArtefactForm(request.POST, request.FILES)
#         if form.is_valid():
#             artefact = form.save(commit=False)
#             artefact.user_last_changes = request.user
#             artefact.save()
#             form.save_m2m()
#
#             messages.success(request, 'Новый артефакт успешно добавлен!')
#             return redirect('artefact_detail', pk=artefact.pk)
#     else:
#         museum_id = request.GET.get('museum')
#         material_id = request.GET.get('material')
#         monument_id = request.GET.get('monument')
#         lead_id = request.GET.get('lead')
#         year_id = request.GET.get('year')
#         histcult_id = request.GET.get('histcult')
#         hallplace_id = request.GET.get('location')
#
#         initial = {}
#         if museum_id:
#             initial['museum'] = museum_id
#         if material_id:
#             initial['material'] = material_id
#         if monument_id:
#             initial['ex_monument'] = monument_id
#         if lead_id:
#             initial['ex_lead'] = lead_id
#         if year_id:
#             initial['year'] = year_id
#         if histcult_id:
#             initial['histcult'] = histcult_id
#         if hallplace_id:
#             initial['location'] = hallplace_id
#
#         form = ArtefactForm(initial=initial)
#
#     return render(request, 'artefacts/add_artefact.html', {'form': form})
def add_artefact(request):
    if request.method == 'POST':
        form = ArtefactForm(request.POST, request.FILES)
        if form.is_valid():
            artefact = form.save(commit=False)
            artefact.user_last_changes = request.user
            artefact.save()
            form.save_m2m()

            messages.success(request, 'Новый артефакт успешно добавлен!')
            return redirect('artefact_detail', pk=artefact.pk)
    else:
        form = ArtefactForm()
    return render(request, 'artefacts/add_artefact.html', {'form': form})
# def add_artefact(request):
#     if request.method == 'POST':
#         form = ArtefactForm(request.POST, request.FILES)
#         if form.is_valid():
#             artefact = form.save(commit=False)
#             artefact.user_last_changes = request.user
#             artefact.save()
#             form.save_m2m()
#             messages.success(request, 'Новый артефакт успешно добавлен!')
#             request.session['form_data'] = None  # очищаем данные формы из сессии
#             return redirect('artefact_detail', pk=artefact.pk)
#         else:
#             messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
#             request.session['form_data'] = form.data.dict()  # сохраняем данные формы в сессию
#     else:
#         initial = {}
#         # восстанавливаем данные формы из сессии
#         form_data = request.session.get('form_data')
#         if form_data:
#             initial.update(form_data)  # добавляем новые значения в initial, не затирая старые
#         else:
#             museum_id = request.GET.get('museum')
#             material_id = request.GET.get('material')
#             monument_id = request.GET.get('monument')
#             lead_id = request.GET.get('lead')
#             year_id = request.GET.get('year')
#             histcult_id = request.GET.get('histcult')
#             hallplace_id = request.GET.get('location')
#             if museum_id:
#                 initial['museum'] = museum_id
#             if material_id:
#                 initial['material'] = material_id
#             if monument_id:
#                 initial['ex_monument'] = monument_id
#             if lead_id:
#                 initial['ex_lead'] = lead_id
#             if year_id:
#                 initial['year'] = year_id
#             if histcult_id:
#                 initial['histcult'] = histcult_id
#             if hallplace_id:
#                 initial['location'] = hallplace_id
#         form = ArtefactForm(initial=initial)
#     return render(request, 'artefacts/add_artefact.html', {'form': form})

def add_hist_cult(request):
    culture_form = CultureForm()
    period_form = HistoricalPeriodForm()
    hc_form = HistoricalCultureForm()
    culture_saved = False
    period_saved = False
    hc_saved = False

    if request.method == 'POST':
        if 'save_culture' in request.POST:
            culture_form = CultureForm(request.POST)

            if culture_form.is_valid():
                culture = culture_form.save()
                culture_saved = True
                url = reverse('add_hist_cult')
                messages.success(request, 'Новая культура добавлена!')
                return redirect(url)
            else:
                messages.error(request, 'Такая культура уже существует или вы ввели цифру!')
        elif 'save_period' in request.POST:
            period_form = HistoricalPeriodForm(request.POST)

            if period_form.is_valid():
                period = period_form.save()
                period_saved = True
                url = reverse('add_hist_cult')
                messages.success(request, 'Новый исторический период добавлен!')
                return redirect(url)
            else:
                messages.error(request, 'Такой исторический период уже существует или вы ввели цифру!')
        elif 'save_hc' in request.POST:
            hc_form = HistoricalCultureForm(request.POST)

            if hc_form.is_valid():
                hc = hc_form.save(commit=False)
                # Проверяем, есть ли значение поля `name_cult`
                if hc.name_cult_id and hc.name_hist_id:
                    hc.save()
                    hc_saved = True
                    url = reverse('add_hist_cult')
                    messages.success(request, 'Новая связь между культурой и историческим периодом добавлена!')
                    return redirect(url)
                else:
                    messages.error(request, 'Пожалуйста, заполните поля для связи .')
            else:
                messages.error(request, 'Такая связь уже существует!')
    else:
        histcult_id = request.GET.get('histcult')
        initial = {'histcult': ''}
        if histcult_id:
            histcult = HistoricalCulture.objects.get(pk=histcult_id)
            initial['histcult'] = histcult_id
        hc_form = HistoricalCultureForm(initial=initial)


    return render(request, 'artefacts/add_hist_cult.html', {
        'culture_form': culture_form,
        'period_form': period_form,
        'hc_form': hc_form,
        'culture_saved': culture_saved,
        'period_saved': period_saved,
        'hc_saved': hc_saved
    })

def add_hall_place(request):
    hall_form = HallForm()
    place_form = PlaceForm()
    hp_form = HallPlaceForm()
    hall_saved = False
    place_saved = False
    hp_saved = False

    if request.method == 'POST':
        if 'save_hall' in request.POST:
            hall_form = HallForm(request.POST)

            if hall_form.is_valid():
                hall = hall_form.save()
                hall_saved = True
                url = reverse('add_hall_place')
                messages.success(request, 'Новый зал добавлен!')
                return redirect(url)
            else:
                messages.error(request, 'Такой зал существует!')
        elif 'save_place' in request.POST:
            place_form = PlaceForm(request.POST)

            if place_form.is_valid():
                place = place_form.save()
                place_saved = True
                url = reverse('add_hall_place')
                messages.success(request, 'Новое расположение добавлено!')
                return redirect(url)
            else:
                messages.error(request, 'Такое расположение существует!')
        elif 'save_hp' in request.POST:
            hp_form = HallPlaceForm(request.POST)

            if hp_form.is_valid():
                hp = hp_form.save(commit = False)
                if hp.name_hall_id and hp.name_place_id:
                    hp.save()
                    hp_saved = True
                    # url = reverse('add_artefact') + '?location={}'.format(hp.pk)
                    url = reverse('add_hall_place')
                    messages.success(request, 'Новая связь  между залом и расположением добавлена!')
                    return redirect(url)
                else:
                    messages.error(request, 'Пожалуйста, заполните поля для связи .')
            else:
                messages.error(request, 'Такая связь существует!')
    else:
        hallplace_id = request.GET.get('location')
        initial = {'location': ''}
        if hallplace_id:
            hallplace = HallPlace.objects.get(pk=hallplace_id)
            initial['location'] = hallplace_id
        hp_form = HallPlaceForm(initial=initial)

    return render(request, 'artefacts/add_hall_place.html', {
        'hall_form': hall_form,
        'place_form': place_form,
        'hp_form': hp_form,
        'hall_saved': hall_saved,
        'place_saved': place_saved,
        'hp_saved': hp_saved
    })


