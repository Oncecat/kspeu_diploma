from django import forms
from . models import Myip

class Descform(forms.ModelForm):
    class Meta:
        model = Myip
        # exclude = ['ip','mac','type','slug']
        fields = ('description',)

