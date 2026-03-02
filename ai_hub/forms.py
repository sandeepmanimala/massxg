from django import forms
from .models import AIModel

class AIModelForm(forms.ModelForm):
    class Meta:
        model = AIModel
        fields = ['name', 'description', 'architecture', 'github_url', 'paper_url', 'huggingface_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
