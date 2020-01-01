from django import forms
from django.contrib.auth import get_user_model

from .models import Snippet, SnippetFlag

User = get_user_model()


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ['title', 'description', 'code', 'language']


class SnippetFlagForm(forms.ModelForm):
    class Meta:
        model = SnippetFlag
        fields = ('flag',)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password1 = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput())
    password2 = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput())

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("This username has been taken.")

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("The two passwords are not same.")
        return self.cleaned_data

    def save(self):
        new_user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'])
        return new_user
