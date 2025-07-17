from django.shortcuts import render, get_object_or_404, redirect
from .models import Idea, IdeaStar
from devtools.models import DevTool
from .forms import IdeaForm  # 나중에 forms.py 만들 예정
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.db.models import Q


from django.core.paginator import Paginator
from django.db.models import Count

def idea_list(request):
    query = request.GET.get('q', '')  # 검색어
    order = request.GET.get('order', 'created_at')

    ideas = Idea.objects.all()

    if query:
        ideas = ideas.filter(
            Q(title__icontains=query) |  # 제목에 포함
            Q(devtool__name__icontains=query)  # 개발툴 이름에 포함 (FK 연관)
        )

    # 정렬 처리
    if order == 'like':
        ideas = ideas.annotate(like_count=Count('ideastar')).order_by('-like_count')
    elif order == 'interest':
        ideas = ideas.order_by('-interest')
    elif order == 'latest':
        ideas = ideas.order_by('-created_at')
    elif order == 'created':
        ideas = ideas.order_by('created_at')  # 등록순 (오래된 → 최신)
    elif order == 'name':
        ideas = ideas.order_by('title')
    else:
        ideas = ideas.order_by('-created_at')

    # 페이지네이션 처리 (한 페이지당 4개)
    paginator = Paginator(ideas, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 찜 상태 처리
    starred_ids = set()
    if request.user.is_authenticated:
        starred_ids = set(IdeaStar.objects.filter(user=request.user).values_list('idea_id', flat=True))
    for idea in page_obj:
        idea.is_starred = idea.id in starred_ids

    return render(request, 'ideas/idea_list.html', {
        'page_obj': page_obj,
        'order': order,
        'query': query,
    })

# 아이디어 상세
def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    is_starred = False
    if request.user.is_authenticated:
        is_starred = IdeaStar.objects.filter(user=request.user, idea=idea).exists()
    idea.is_starred = is_starred

    return render(request, 'ideas/idea_detail.html', {'idea': idea})

# 아이디어 등록
def idea_add(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.save()
            return redirect('ideas:idea_detail', pk=idea.pk)
    else:
        form = IdeaForm()
    return render(request, 'ideas/idea_form.html', {'form': form})

# 아이디어 수정
def idea_edit(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            form.save()
            return redirect('ideas:idea_detail', pk=idea.pk)
    else:
        form = IdeaForm(instance=idea)
    return render(request, 'ideas/idea_form.html', {'form': form})

# 아이디어 삭제
def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.delete()
    return redirect('ideas:idea_list')

# 찜하기 (AJAX)
def idea_star(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    star, created = IdeaStar.objects.get_or_create(user=request.user, idea=idea)
    if not created:
        star.delete()
        starred = False
    else:
        starred = True
    return JsonResponse({'starred': starred, 'star_count': IdeaStar.objects.filter(idea=idea).count()})

# 관심도 +/-
def idea_interest(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    action = request.POST.get('action')
    if action == 'plus':
        idea.interest += 1
    elif action == 'minus' and idea.interest > 0:
        idea.interest -= 1
    idea.save()
    return JsonResponse({'interest': idea.interest})

from django.conf import settings

def ajax_search(request):
    query = request.GET.get('q', '')
    ideas_qs = Idea.objects.filter(
        Q(title__icontains=query) | Q(devtool__name__icontains=query)
    ).values('id', 'title', 'devtool__name', 'image')

    ideas = []
    for idea in ideas_qs:
        if idea['image']:
            idea['image'] = settings.MEDIA_URL + idea['image']
        else:
            idea['image'] = '/static/default.jpg'  # 없을 때 기본 이미지 (선택)
        ideas.append(idea)

    return JsonResponse({'ideas': ideas})