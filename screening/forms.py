from django import forms
from .models import Resume
from django.contrib.auth.models import User

class ResumeForm(forms.ModelForm):
    job_description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Resume
        fields = ['file', 'job_description']


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']