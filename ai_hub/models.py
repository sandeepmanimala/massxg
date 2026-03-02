from django.db import models
from django.contrib.auth.models import User

class AIModel(models.Model):
    ARCHITECTURE_CHOICES = [
        ('text', 'Text / LLM'),
        ('vision', 'Vision / CNN / ViT'),
        ('graph', 'Graph Neural Network'),
        ('diffusion', 'Diffusion / Generative'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    architecture = models.CharField(max_length=50, choices=ARCHITECTURE_CHOICES)
    github_url = models.URLField(blank=True, null=True, help_text="Link to the source code repository")
    paper_url = models.URLField(blank=True, null=True, help_text="Link to the associated research paper")
    huggingface_url = models.URLField(blank=True, null=True, help_text="Link to HuggingFace or model weights")
    
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.get_architecture_display()})"
    
    class Meta:
        ordering = ['-uploaded_at']

class ModelResource(models.Model):
    RESOURCE_TYPES = [
        ('tutorial', 'Tutorial / Guide'),
        ('notebook', 'Jupyter Notebook'),
        ('dataset', 'Training Dataset Link'),
    ]
    
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    content = models.TextField(help_text="Markdown content or brief description")
    external_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} for {self.ai_model.name}"
