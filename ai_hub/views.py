from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AIModel
from .forms import AIModelForm

def ai_list(request):
    query = request.GET.get('q', '')
    architecture = request.GET.get('architecture', '')

    models = AIModel.objects.all()

    if query:
        models = models.filter(name__icontains=query) | models.filter(description__icontains=query)
    
    if architecture:
        models = models.filter(architecture=architecture)

    return render(request, 'ai_hub/list.html', {
        'models': models,
        'query': query,
        'selected_architecture': architecture,
        'architectures': AIModel.ARCHITECTURE_CHOICES
    })

def ai_detail(request, pk):
    ai_model = get_object_or_404(AIModel, pk=pk)
    return render(request, 'ai_hub/detail.html', {'ai_model': ai_model})

@login_required
def ai_submit(request):
    if request.method == 'POST':
        form = AIModelForm(request.POST)
        if form.is_valid():
            ai_model = form.save(commit=False)
            ai_model.uploaded_by = request.user
            ai_model.save()
            return redirect('ai_hub:detail', pk=ai_model.pk)
    else:
        form = AIModelForm()
    return render(request, 'ai_hub/submit.html', {'form': form})
