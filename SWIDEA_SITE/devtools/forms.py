from django import forms
from .models import DevTool

class DevToolForm(forms.ModelForm):
    class Meta:
        model = DevTool
        fields = ['name', 'kind', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'kind': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
