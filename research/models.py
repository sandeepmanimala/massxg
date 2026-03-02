from django.db import models
from django.contrib.auth.models import User

class ResearchPaper(models.Model):
    FIELD_CHOICES = [
        ('bioinformatics', 'Bioinformatics'),
        ('systems_biology', 'Systems Biology'),
        ('genomics', 'Genomics & Epigenomics'),
        ('proteomics', 'Proteomics'),
        ('clinical', 'Clinical Informatics'),
    ]

    title = models.CharField(max_length=500)
    authors = models.CharField(max_length=500, help_text="Comma-separated authors")
    abstract = models.TextField()
    field = models.CharField(max_length=50, choices=FIELD_CHOICES)
    pdf_file = models.FileField(upload_to='research_papers/%Y/%m/')
    
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    doi = models.CharField(max_length=100, blank=True, null=True, help_text="Digital Object Identifier")
    read_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-uploaded_at']
