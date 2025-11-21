# ~/automation/fullstack_ztp/ztp/views.py

from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from . import models
from .utility_functions import create_host_file, create_playbook, run_playbook, update_inventory

# Create your views here.

from .forms import SCPServerForm, DHCPServerForm, HostForm, AutomationForm


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

def edit_host_view(request, id):
    obj = models.Host.objects.get(id=id)
    form = HostForm(initial=obj.__dict__)
    if request.method == "POST":
        form = HostForm(request.POST)        
        if form.is_valid():
            user_data = form.cleaned_data
            obj.hostname = user_data['hostname']
            obj.mgmt_ip = user_data['mgmt_ip']
            obj.vendor = user_data['vendor']
            obj.model = user_data['model']
            obj.device_username = user_data['device_username']
            obj.device_password = user_data['device_password']
            obj.auth_type = user_data['auth_type']
            obj.save()
            return redirect(reverse('homepage'))
    return render(request, 'ztp/edit_host.html', {'form': form})


def list_hosts_view(request):
    hosts = models.Host.objects.all()
    return render(request, 'ztp/list_hosts.html', {'hosts': hosts})


def delete_host_view(request, id):
    obj = models.Host.objects.get(id=id)
    obj.delete()
    return redirect(reverse('list_hosts'))


def automation_view(request):
    form = AutomationForm()  

    if request.method == "POST":
        host = models.Host.objects.get(id=request.POST.get('hostname'))
        ##### Step 1: Create Host File
        create_host_file(host=host)
        playbook_path = '/automation/ansible_automation/final_project_generate_ztp_configs.yml'
        create_playbook(hostname=host.hostname, 
                        tftp_server=models.DHCPServer.objects.first().ip_address,
                        playbook_path=playbook_path
                        )
        ##### Step 2: Update Inventory File
        update_inventory(host=host)
        ##### Step 3: Run playbook
        ###### Step 3.1: PLAY 1: Create Configurations for Cisco Devices
        ###### Step 3.2: PLAY 2: Transfer device configs to TFTP Server
        ###### Step 3.3: PLAY 3: Configure TFTP/DHCP Servers        
        run_playbook(playbook_path=playbook_path, inventory_path="/automation/ztp/hosts")        

        return render(request, 'ztp/success.html')

    return render(request, 'ztp/automation.html', {'form': form})