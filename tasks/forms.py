from django.forms import ModelForm, TextInput, Textarea, CheckboxInput
from .models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','important']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'important': CheckboxInput(attrs={'class': 'form-check-input'}),
        }