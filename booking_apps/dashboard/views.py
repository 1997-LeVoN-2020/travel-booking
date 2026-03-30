from django.shortcuts import render

def dashboard(request):
    context = {
        'title': 'Главная страница',
        'message': 'Добро пожаловать на сайт!',
    }
    return render(request, 'booking_apps/base.html', context)