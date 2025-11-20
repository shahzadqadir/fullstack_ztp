# ~/automation/fullstack_ztp/ztp/views.py

from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from . import models

# Create your views here.

from .forms import SCPServerForm, DHCPServerForm, HostForm    # New import HostForm


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


def delete_scp_server_view(request, id):
    obj = models.SCPServer.objects.get(id=id)
    obj.delete()
    return redirect(reverse('list_scp_servers'))


def create_dhcp_server_view(request):
    form = DHCPServerForm()
    if request.method == "POST":
        form = DHCPServerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('homepage'))
    return render(request, 'ztp/create_dhcp_server.html', {'form': form})

def list_dhcp_servers_view(request):
    dhcp_servers = models.DHCPServer.objects.all()
    return render(request, 'ztp/list_dhcp_servers.html', {'dhcp_servers': dhcp_servers})


def edit_dhcp_server_view(request, id):
    obj = models.DHCPServer.objects.get(id=id)
    form = DHCPServerForm(instance=obj)
    if request.method == "POST":
        form = DHCPServerForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('list_dhcp_servers'))
    return render(request, 'ztp/edit_dhcp_server.html', {'form': form})


def delete_dhcp_server_view(request, id):
    obj = models.DHCPServer.objects.get(id=id)
    obj.delete()
    return redirect(reverse('list_dhcp_servers'))


def create_host_view(request):  # NEW
    form = HostForm()
    if request.method == "POST":
        form = HostForm(request.POST)
        if form.is_valid():
            models.Host.objects.create(
                hostname=request.POST.get('hostname'),
                mgmt_ip=request.POST.get('mgmt_ip'),
                vendor=request.POST.get('vendor'),
                model=request.POST.get('model'),
                device_username=request.POST.get('device_username'),
                device_password=request.POST.get('device_password'),
                auth_type=request.POST.get('auth_type'),
            ).save()
            return redirect(reverse('homepage'))
    return render(request, 'ztp/create_host.html', {'form': form})