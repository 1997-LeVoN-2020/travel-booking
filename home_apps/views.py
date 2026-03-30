from django.shortcuts import render

def home(request):
    context = {
        'title': 'Главная страница',
        'message': 'Добро пожаловать на сайт!',
    }
    return render(request, 'home_apps/base.html', context)