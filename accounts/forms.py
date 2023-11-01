from django import forms
from .models import User, UserProfile
from .validators import allow_only_images_validator


class UserForm(forms.ModelForm):
   
    password = forms.CharField(widget = forms.PasswordInput())
    confirm_password = forms.CharField(widget = forms.PasswordInput())
    
    class Meta:
        model= User
        fields= ['first_name','last_name', 'email','username', 'phone_number','password']
        
        
        
class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing...', 'required': 'required'}))
    cover_photo =  forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[allow_only_images_validator])
    profile_picture =  forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[allow_only_images_validator])
    
    latitude =forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))                         
    longitude = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
        
     
    class Meta:
        model = UserProfile
        fields= ['profile_picture','cover_photo','address','country','state','city','pin_code','latitude','longitude']
       
       
    #   latitude و   برای گرفتن  longitude (مختصات جغرافیایی)
    
    # def __init__ (self,*args, **kwargs):
    #     super(UserProfile,self).__init__(*args,**kwargs)
    #     for field in self.fields:
    #         if field == 'latitude' or field == 'longitude':
    #             self.fields[field].widget.arttrs['readonly'] = 'readonly'
                