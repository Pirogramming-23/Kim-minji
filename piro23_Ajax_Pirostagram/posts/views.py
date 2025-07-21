from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, Comment, Like, PostImage

# 피드(게시물 리스트)
def post_list(request):
    sort = request.GET.get('sort', 'latest')  # 기본은 latest
    posts = Post.objects.all()

    if sort == 'latest':
        posts = posts.order_by('-created_at')
    elif sort == 'likes':
        posts = sorted(posts, key=lambda p: p.likes.count(), reverse=True)
    elif sort == 'comments':
        posts = sorted(posts, key=lambda p: p.comments.count(), reverse=True)

    return render(request, 'posts/post_list.html', {'posts': posts})

@login_required
def like_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        if not post_id or not post_id.isdigit():
            return JsonResponse({'error': 'Invalid post_id'}, status=400)
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

@login_required
def add_comment(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')
        if not post_id or not post_id.isdigit() or not content.strip():
            return JsonResponse({'error': 'Invalid data'}, status=400)
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
        images = request.FILES.getlist('images')
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            for img in images:
                PostImage.objects.create(post=post, image=img)
            return redirect('posts:post_list')
    else:
        form = PostForm()
    return render(request, 'posts/post_create.html', {'form': form})