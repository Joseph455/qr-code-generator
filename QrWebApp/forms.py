from django import forms
from django.forms.forms import Form
import  os

class RequestForm(forms.Form):
    url = forms.URLField(max_length=300, help_text="Enter the url", required=True)
    
    email = forms.EmailField(
        max_length=150,
        required=True,
        error_messages={
            "null": "enter a valid email address",
            "blank": "Enter a valid email address",
            "invalid": "Enter a valid email address",
            "required": "Email Field is required",
    })
    
    Choices = (("svg", "svg"), ("png", "png"), ("jpeg", "jpeg"))
    type =  forms.ChoiceField(choices=Choices, required=True)
