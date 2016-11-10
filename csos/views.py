from django.shortcuts import render


def index(request):
    return reversals(request)


def reversals(request):
    return render(request, 'lake_reversals.html')