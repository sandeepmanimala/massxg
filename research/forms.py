from django import forms
from .models import ResearchPaper

class ResearchPaperForm(forms.ModelForm):
    class Meta:
        model = ResearchPaper
        fields = ['title', 'authors', 'abstract', 'field', 'doi', 'pdf_file']
        widgets = {
            'abstract': forms.Textarea(attrs={'rows': 6}),
        }
