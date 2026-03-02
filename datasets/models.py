from django.db import models
from django.contrib.auth.models import User

class Dataset(models.Model):
    CATEGORY_CHOICES = [
        ('genomics', 'Genomics'),
        ('proteomics', 'Proteomics'),
        ('metabolomics', 'Metabolomics'),
        ('cells', 'Cells / Single-Cell'),
        ('tissues', 'Tissues / Spatial'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="datasets")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='datasets/%Y/%m/%d/')
    file_size_bytes = models.BigIntegerField(default=0, help_text="Size of the dataset in bytes")
    is_public = models.BooleanField(default=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma separated tags")

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title
