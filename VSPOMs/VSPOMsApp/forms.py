from django import forms

class SettingsForm(forms.Form):
    dispersal_kernel = forms.IntegerField()
    connectivity_function = forms.IntegerField()
    colonization_function = forms.IntegerField()
