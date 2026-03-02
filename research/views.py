from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ResearchPaper
from .forms import ResearchPaperForm

def paper_list(request):
    query = request.GET.get('q', '')
    field = request.GET.get('field', '')

    papers = ResearchPaper.objects.all()

    if query:
        papers = papers.filter(title__icontains=query) | papers.filter(authors__icontains=query) | papers.filter(abstract__icontains=query)
    
    if field:
        papers = papers.filter(field=field)

    return render(request, 'research/list.html', {
        'papers': papers,
        'query': query,
        'selected_field': field,
        'fields': ResearchPaper.FIELD_CHOICES
    })

def paper_detail(request, pk):
    paper = get_object_or_404(ResearchPaper, pk=pk)
    
    # Increment read count
    paper.read_count += 1
    paper.save(update_fields=['read_count'])
    
    return render(request, 'research/detail.html', {'paper': paper})

@login_required
def paper_submit(request):
    if request.method == 'POST':
        form = ResearchPaperForm(request.POST, request.FILES)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.uploaded_by = request.user
            paper.save()
            return redirect('research:detail', pk=paper.pk)
    else:
        form = ResearchPaperForm()
    return render(request, 'research/submit.html', {'form': form})
