from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    thumbnail = models.URLField(blank=True, null=True, help_text="Image URL for the course thumbnail")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_level_display()})"
    
    class Meta:
        ordering = ['created_at']

class VideoLesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_url = models.URLField(help_text="YouTube embed code or direct video URL")
    order = models.PositiveIntegerField(default=0)
    duration = models.CharField(max_length=50, blank=True, help_text="e.g., 10:45")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}. {self.title}"
