# ~/automation/fullstack_ztp/fullstack_ztp/views.py

from django.shortcuts import render


def homepage(request):
    return render(request, 'index.html')