from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import ModelForm

from .models import Post,Rating,Profile




class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    
    
    class  Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')


class PostForm(ModelForm):
    
    class Meta:
        model = Post
        fields = ['screenshot','title','description','live_link' ]
        
class RatingForm(ModelForm):
    
    class Meta:
        model = Rating
        fields = ['design_rating','usability_rating','content_rating' ]
        widgets = {
            'design_rating':forms.NumberInput(attrs={'type':'range', 'step': '0.5', 'min': '0', 'max': '10','onchange':'updateTextInput(this.value)','class':'slider'}),
            'usability_rating':forms.NumberInput(attrs={'type':'range', 'step': '0.5', 'min': '0', 'max': '10','onchange':'updateTextInput(this.value)','class':'slider'}),
            'content_rating':forms.NumberInput(attrs={'type':'range', 'step': '0.5', 'min': '0', 'max': '10','onchange':'updateTextInput(this.value)','class':'slider'}),
        }
        
        
class ProfileForm(ModelForm):
    
    class Meta:
        model = Profile
        fields = ['profile_pic','bio','location' ]