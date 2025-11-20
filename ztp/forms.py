# ~/automation/fullstack_ztp/ztp/forms.py

from django import forms

from . import models

class SCPServerForm(forms.ModelForm):
    class Meta:
        model = models.SCPServer
        fields = '__all__'