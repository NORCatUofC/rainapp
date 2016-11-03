from django.shortcuts import render


def index(request):
    return render(request, 'show_event.html')
