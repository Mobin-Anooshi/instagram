from typing import Any
from django import forms
from accounts.models import User
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password',widget=forms.PasswordInput)
    
    class Meta :
        model = User
        fields =('username','profile','bio','full_name','email','birthday',)
        
    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1']!= cd['password2'] :
            raise ValidationError('password must match')
        return cd['password2']
    def save(self, commit:True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit :
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    class Meta :
        model = User
        fields = ('username','profile','bio','full_name','email','birthday','is_active','is_admin')
        

class UserRegistertionForm(forms.Form):
    profile = forms.ImageField(required=False)
    username = forms.CharField()
    # bio = forms.CharField()
    full_name = forms.CharField()
    email = forms.EmailField()
    birthday = forms.DateField()
    password1 = forms.CharField(label='password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password',widget=forms.PasswordInput)
    
    def clean(self) :
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError('password must match')
        
        
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user.exists() :
            raise ValidationError('this email is already exists')
        return email
        
class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    
class UserEditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',
                  'profile',
                  'bio',
                  'full_name',
                  'birthday',
                  'privet',)
    
    