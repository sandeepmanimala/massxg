from django.db import models
from django.contrib.auth.models import User

class Workflow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workflows')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.user.username}"

class Node(models.Model):
    NODE_TYPES = [
        ('dataset', 'Dataset Input'),
        ('model', 'AI Model Execution'),
        ('process', 'Data Processing'),
        ('output', 'Visual Output')
    ]
    
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='nodes')
    type = models.CharField(max_length=50, choices=NODE_TYPES)
    label = models.CharField(max_length=255)
    
    # Store reference IDs dynamically since a node might point to a Dataset or an AIModel
    reference_id = models.IntegerField(null=True, blank=True)
    
    # Canvas positioning coordinates
    pos_x = models.FloatField(default=0)
    pos_y = models.FloatField(default=0)

    def __str__(self):
        return f"{self.type} - {self.label}"

class Edge(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='edges')
    source = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='outgoing_edges')
    target = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='incoming_edges')
    
    def __str__(self):
        return f"{self.source.label} -> {self.target.label}"
