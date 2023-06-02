from django.shortcuts import render

# Create your views here.
def info_about_arts(request):
    return render(request, 'artefacts/info_about_arts.html', {  })