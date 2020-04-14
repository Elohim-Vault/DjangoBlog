from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .form import PostForm
from django.contrib.auth.decorators import login_required


def post_list(request):
    search = request.GET.get('search')

    if search:
        posts = Post.objects.filter(title__icontains=search)
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'posts': post})

@login_required
def post_new(request):
    form = PostForm(request.POST)

    if form.is_valid():
        post = form.save(commit=False)
        post.published_date = timezone.now()
        post.author = request.user
        form.save()
        return redirect("post_detail", pk=post.pk)

    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        post.delete()
        return redirect(post_list)
    else:
        return render(request, 'blog/post_delete.html', {'post':post})


