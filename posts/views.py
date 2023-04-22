from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView

from .forms import PostCreateForm, CommentForm
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
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        new_comment = comment_form.save(commit=False)
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        new_comment.post = post
        new_comment.save()
    else:
        comment_form = CommentForm()
    posts = Post.objects.all()
    logged_user = request.user
    return render(request, 'posts/feed.html', {'posts': posts, 'logged_user': logged_user, 'comment_form': comment_form})


def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    if post.like_by.filter(id=request.user.id).exists():
        post.like_by.remove(request.user)
    else:
        post.like_by.add(request.user)
    return redirect('feed')


class PostDetailView(DetailView):
    template_name = 'posts/post_view.html'
    model = Post


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/post_update.html'

    def get_success_url(self):
        return reverse_lazy('post_view', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data()
        context['title'] = 'Просмотр фото'
        return context


class PostDeleteView(DeleteView):
    template_name = 'posts/post_confirm_delete.html'
    model = Post
    context_object_name = 'post'
    success_url = reverse_lazy('feed')


def post_list_and_create(request):
    qs = Post.objects.all()
    return render(request, 'posts/main.html', {'qs': qs})


def load_post_data_view(request, num_posts):
    visible = 3
    upper = num_posts
    lower = upper - visible
    size = Post.objects.all().count()

    qs = Post.objects.all()
    data = []
    for obj in qs:
        item = {
            'id': obj.id,
            'title': obj.title,
            'body': obj.body,
            'liked': True if request.user in obj.liked.all() else False,
            'count': obj.like_count,
            'author': obj.author.user.username
        }
        data.append(item)
    return JsonResponse({'data': data[lower: upper], 'size': size})


def post_view(request):
    return JsonResponse({'text': 'post'})
