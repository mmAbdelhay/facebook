from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required, permission_required


@login_required(login_url="/login")
@permission_required(["posts.view_post"], raise_exception=True)
def index(request):
    # posts = Post.objects.filter(relation__field__options=["IT", "DevOps"]).all() wbtrg3 array
    posts = Post.objects.all()
    return render(request, 'posts/index.html', {
        "posts": posts
    })

@login_required
def create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'posts/create.html', {
        'form': form
    })


def edit(request, id):
    post = Post.objects.get(pk=id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'posts/edit.html', {
        'form': form,
        'post': post
    })


def delete(request, id):
    post = Post.objects.get(pk=id)
    post.delete()
    return redirect('index')
