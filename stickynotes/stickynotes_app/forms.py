'''This file includes the forms used on my site to
login & register user, and to write a new sticky note.'''

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from .models import StickyNote, Profile


class LoginForm(forms.Form):
    '''Class defining the login form'''
    email_address = forms.EmailField
    password = forms.CharField(widget=forms.PasswordInput())


class RegistrationForm(UserCreationForm):
    '''Model defining the registration form for the user'''
    email = forms.EmailField(required=True)

    class Meta:
        '''
        Meta class for the form.
        Attributes:
        model (Model): The model that this form is associated with.
        fields (tuple): The fields from the model to include in the form.
                        These fields are 'username', 'email', 'password1', and 'password2'.'''
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class StickyNoteForm(forms.ModelForm):
    '''Model defining each sticky note.'''
    class Meta:
        '''
        Meta class for StickyNoteForm.
        Attributes:
            model (Model): The model that this form is associated with.
            fields (tuple): The fields from the model to include in the form. 
                            These fields are 'title' and 'body'.
        '''
        model = StickyNote
        fields = ['title', 'body', 'color']
        widgets = {
            'color': forms.Select(choices=StickyNote.COLOR_CHOICES)
        }
        

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date']