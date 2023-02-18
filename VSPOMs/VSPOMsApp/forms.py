from django import forms
from .models import VSPOMs

class SettingsForm(forms.ModelForm):
    class Meta:
        model = VSPOMs
        fields = ['dispersal_kernel', 'connectivity', 'colonization', 'extinction', 'extinction_rescue', 'stochasticity']
