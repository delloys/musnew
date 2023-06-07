from django.urls import path,include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.info_about_arts), name='info_about_arts'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('artefact/<int:pk>', login_required(views.artefact_detail), name='artefact_detail'),
    path('artefact/new/', login_required(views.add_artefact), name='add_artefact'),
    path('add_museum/', login_required(views.add_museum), name='add_museum'),
    path('add_material/', login_required(views.add_material), name='add_material'),
    path('add_ex_monument/', login_required(views.add_ex_monument), name='add_ex_monument'),
    path('add_ex_lead/', login_required(views.add_ex_lead), name='add_ex_lead'),
    path('add_year/', login_required(views.add_year), name='add_year'),
    path('add_hist_cult/', login_required(views.add_hist_cult), name='add_hist_cult'),
    path('add_hall_place/', login_required(views.add_hall_place), name='add_hall_place'),
    path('artefacts/edit/<int:pk>/', login_required(views.edit_artefact), name='edit_artefact'),
    path('artefact/<int:pk>/delete/', login_required(views.delete_artefact), name='delete_artefact'),
]