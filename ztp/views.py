# ~/automation/fullstack_ztp/ztp/views.py

from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from .forms import SCPServerForm
from . import models

def create_scp_server_view(request):
    form = SCPServerForm()
    if request.method == "POST":
        form = SCPServerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('homepage'))
    return render(request, 'ztp/create_scp_server.html', {'form': form})


def list_scp_servers_view(request):
    scp_servers = models.SCPServer.objects.all()
    return render(request, 'ztp/list_scp_servers.html', {'scp_servers': scp_servers})


def edit_scp_server_view(request, id):
    obj = models.SCPServer.objects.get(id=id)
    form = SCPServerForm(instance=obj)
    if request.method == "POST":
        form = SCPServerForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('list_scp_servers'))
    return render(request, 'ztp/edit_scp_server.html', {'form': form})


def delete_scp_server_view(request, id):	# NEW
    obj = models.SCPServer.objects.get(id=id)
    obj.delete()
    return redirect(reverse('list_scp_servers'))