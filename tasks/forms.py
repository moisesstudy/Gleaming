#from django.forms import ModelForm     # esto es una clase
from django import forms               
from .models import Task                # importamos el modelo de Task

#class TaskForm(ModelForm):
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task                                    # Este formulario esta basado en Task  (Que esta importado arriba)
        fields = ['title', 'description', 'important']  # indico los campos que me interesan
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'write a title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder' : 'write a description'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'})
        }
