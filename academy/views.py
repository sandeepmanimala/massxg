from django.shortcuts import render, get_object_or_404
from .models import Course, VideoLesson

def course_list(request):
    query = request.GET.get('q', '')
    level = request.GET.get('level', '')

    courses = Course.objects.all()

    if query:
        courses = courses.filter(title__icontains=query) | courses.filter(description__icontains=query)
    
    if level:
        courses = courses.filter(level=level)

    return render(request, 'academy/list.html', {
        'courses': courses,
        'query': query,
        'selected_level': level,
        'levels': Course.LEVEL_CHOICES
    })

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    # Get active video if specified, else use the first one
    video_id = request.GET.get('v')
    
    lessons = course.lessons.all()
    active_lesson = None
    if video_id:
        active_lesson = lessons.filter(id=video_id).first()
    
    if not active_lesson and lessons:
        active_lesson = lessons.first()

    return render(request, 'academy/detail.html', {
        'course': course,
        'lessons': lessons,
        'active_lesson': active_lesson
    })
