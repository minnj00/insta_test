from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

# Create your views here.

def index(request):
    posts = Post.objects.all().order_by('-id')
    comment_form = CommentForm()

    context = {
        'posts': posts,
        'comment_form': comment_form,

    }
    return render(request, 'index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:index')
    else:
        form = PostForm()
    context={
        'form': form,
    }

    return render(request, 'form.html', context)

@login_required
def comment_create(request, post_id):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        post = Post.objects.get(id=post_id)
        comment.post = post
        comment.save()
        return redirect('posts:index')
        
@login_required       
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    if post in user.like_posts.all():
        post.like_users.remove(user)
    else:
        post.like_users.add(user)

    return redirect('posts:index')

def like_async(request, post_id):
    # context = {
    #     'message': post_id,
    # }

    user = request.user
    post = Post.objects.get(id=post_id)

    if user in post.like_users.all():
        post.like_users.remove(user)
        status = False # 좋아요 취소
    else:
        post.like_users.add(user)
        status = True # 좋아요 실행

    context = {
        'status': status,
        'count':len(post.like_users.all())
    }
    
    return JsonResponse(context) # 문서를 return 하지 않고 그 데이터만 return 함.


def comment_update(request, post_id, id):
    comment = Comment.objects.get(id=id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            context = {
                'newContent': comment.content,
                'user': comment.user.username,
            }
        else:
            context = {
                'message': 'fail'
            }

        return JsonResponse(context)
    else:
        form = CommentForm(instance=comment)

    return HttpResponse(form)

