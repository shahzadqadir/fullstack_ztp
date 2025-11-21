# ~/automation/fullstack_ztp/ztp/forms.py

from django import forms
from . import models

class SCPServerForm(forms.ModelForm):
    class Meta:
        model = models.SCPServer
        fields = '__all__'


class DHCPServerForm(forms.ModelForm):
    class Meta:
        model = models.DHCPServer
        fields = '__all__'


class HostForm(forms.Form):
    hostname = forms.CharField()
    mgmt_ip = forms.CharField()
    vendor = forms.ChoiceField(choices=[('cisco', 'Cisco'), 
                                        ('juniper','Juniper'),
                                        ('fortigate', 'Fortigate')])
    model = forms.CharField()
    device_username = forms.CharField()
    device_password = forms.CharField(widget=forms.PasswordInput())
    auth_type = forms.ChoiceField(choices=[('local', 'Local'),])


class AutomationForm(forms.Form):   # NEW
    hostname = forms.ModelChoiceField(queryset=models.Host.objects.all())
    scp_server = forms.ModelChoiceField(queryset=models.SCPServer.objects.all())
    dhcp_server = forms.ModelChoiceField(queryset=models.DHCPServer.objects.all())