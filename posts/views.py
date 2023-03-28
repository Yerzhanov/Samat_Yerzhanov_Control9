from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostCreateForm
from django.contrib.auth.decorators import login_required
from .models import Post

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            return redirect('feed')
    else:
        form = PostCreateForm(data=request.POST)
    return render(request, 'posts/create.html', {'form': form})


def feed(request):
    posts = Post.objects.all()
    logged_user = request.user
    return render(request, 'posts/feed.html', {'posts': posts, 'logged_user': logged_user})


def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    if post.like_by.filter(id=request.user.id).exists():
        post.like_by.remove(request.user)
    else:
        post.like_by.add(request.user)
    return redirect('feed')

