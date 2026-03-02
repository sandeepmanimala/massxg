from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Dataset
from .forms import DatasetUploadForm

def dataset_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    datasets = Dataset.objects.filter(is_public=True).order_by('-uploaded_at')

    if query:
        datasets = datasets.filter(title__icontains=query) | datasets.filter(description__icontains=query)
    
    if category:
        datasets = datasets.filter(category=category)

    return render(request, 'datasets/list.html', {
        'datasets': datasets,
        'query': query,
        'selected_category': category,
        'categories': Dataset.CATEGORY_CHOICES
    })

def dataset_detail(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    # Check permissions (either public or user owns it)
    if not dataset.is_public and dataset.uploaded_by != request.user:
        return redirect('datasets:list')
    
    return render(request, 'datasets/detail.html', {'dataset': dataset})

@login_required
def dataset_upload(request):
    if request.method == 'POST':
        form = DatasetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.uploaded_by = request.user
            if dataset.file:
                dataset.file_size_bytes = request.FILES['file'].size
            dataset.save()
            return redirect('datasets:detail', pk=dataset.pk)
    else:
        form = DatasetUploadForm()
    return render(request, 'datasets/upload.html', {'form': form})
