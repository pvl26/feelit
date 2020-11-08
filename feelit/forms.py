from django import forms

class ReceveImage(forms.Form):
    image = forms.ImageField()
