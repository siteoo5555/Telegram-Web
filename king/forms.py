from django import forms
from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model= User
        fields =['username', 'address', 'password', 'email', 'phone_number','country','gender','age',]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =['username','phone_number','bio','birthday',]

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']

class ChatNameForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['name', 'description','photo',]

class ChatMembersForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(queryset=User.objects.all(),widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Chat
        fields = ['members']


class MessagesForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['sms',]

class LoginForm(forms.Form):
    username = forms.CharField(max_length=35)
    password = forms.CharField(max_length=25)

class PasswordForm(forms.Form):
    old_password = forms.CharField(max_length=15)
    new_password = forms.CharField(max_length=15)
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','phone_number']    
class Create_Friend_ChatForm(forms.ModelForm):
    class Meta:
        model = None
        fields = []