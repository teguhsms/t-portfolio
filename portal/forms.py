from django import forms
from portal.models import UploadModel

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadModel
