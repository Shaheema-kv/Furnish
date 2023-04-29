from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from order.models import Address

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control','required':False}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','required':False}),
            

        }
        

class UserProfileForm(forms.ModelForm): 
    profile_picture = forms.ImageField(required=False,  error_messages={'invalid':("Image files only")}, widget=forms.FileInput(attrs={ 'hidden': True ,'id': 'upload'}))
    class Meta:
        model = UserProfile
        fields = ("address_line_1","address_line_2","email","phone","city","state","country","profile_picture" )
        widgets = {
            'address_line_1': forms.TextInput(attrs={'class': 'form-control', 'required':False }),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control','required':False}),
            'phone': forms.TextInput(attrs={'class': 'form-control','required':False}),
            'city': forms.TextInput(attrs={'class': 'form-control','required':False}),
            'state': forms.TextInput(attrs={'class': 'form-control','required':False}),
            'country': forms.TextInput(attrs={'class': 'form-control','required':False}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control',}),
            'email': forms.TextInput(attrs={'class': 'form-control','required':False}),

        }
        

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('first_name', 'last_name','address','email','phone','city','state','country','postal_code')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control',}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',}),
            'address': forms.TextInput(attrs={'class': 'form-control','required': True }),
            'phone': forms.TextInput(attrs={'class': 'form-control',}),
            'email': forms.TextInput(attrs={'class': 'form-control',}),
            'city': forms.TextInput(attrs={'class': 'form-control',}),
            'state': forms.TextInput(attrs={'class': 'form-control',}),
            'country': forms.TextInput(attrs={'class': 'form-control',}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control',}),

            
            
            

        }
        

        



