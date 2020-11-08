from django import  forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'image','description', 'email', 'phone', 'website', 'instagram', 'twitter', 'facebook']

        widget = {
            'description' : forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'full_name' : 'Full Name'
        }
