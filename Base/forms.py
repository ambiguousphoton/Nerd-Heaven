from django.forms import ModelForm
from .models import Island

class Island_Form(ModelForm):
    class Meta:
        model = Island
        fields = '__all__'