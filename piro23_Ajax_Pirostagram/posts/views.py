from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, Comment, Like

# 피드(게시물 리스트)
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/post_list.html', {'posts': posts})


# 좋아요 토글 (Ajax)
@login_required
def like_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(post=post, user=request.user)

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        like_count = post.likes.count()
        return JsonResponse({'liked': liked, 'like_count': like_count})

    return JsonResponse({'error': 'Invalid request'}, status=400)


# 댓글 작성 (Ajax)
@login_required
def add_comment(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')
        post = get_object_or_404(Post, id=post_id)

        comment = Comment.objects.create(post=post, user=request.user, content=content)

        return JsonResponse({
            'comment_id': comment.id,
            'username': comment.user.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


# 댓글 삭제 (Ajax)
@login_required
def delete_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id, user=request.user)
        comment.delete()
        return JsonResponse({'deleted': True})

    return JsonResponse({'error': 'Invalid request'}, status=400)

from django.contrib.auth.decorators import login_required
from .forms import PostForm

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:post_list')
    else:
        form = PostForm()
    return render(request, 'posts/post_create.html', {'form': form})