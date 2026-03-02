from django import forms
from .models import Dataset

class DatasetUploadForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['title', 'description', 'category', 'file', 'tags', 'is_public']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
