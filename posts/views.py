from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Group
from .forms import PostForm

User = get_user_model()


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'posts/index.html',
                  {'page': page, 'post_list': post_list})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_posts.all().order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  'posts/group.html',
                  {'group': group, 'page': page, 'posts': posts}
                  )


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:posts_index')
    form = PostForm()
    return render(request, 'posts/new_post.html', {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    author_posts = Post.objects.filter(author=author).order_by('-pub_date')
    posts_count = author_posts.count()
    paginator = Paginator(author_posts, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'author': author,
        'page': page,
        'posts_count': posts_count,
    }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    author_posts = Post.objects.get(id=post_id)
    posts_count = Post.objects.filter(author=author).count()
    context = {
        'author': author,
        'author_posts': author_posts,
        'posts_count': posts_count,
        'post_id': post_id,
    }
    return render(request, 'post.html', context)


@login_required
def post_edit(request, username, post_id):
    username = get_object_or_404(User, username=username)
    post = Post.objects.get(author=username, id=post_id)
    if request.user == username:
        post = Post.objects.get(author=username, id=post_id)
        form = PostForm(instance=post)
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form = form.save(commit=False)
                form.save()
            return redirect('posts:post', username=username, post_id=post.id)
        return render(request, 'new_post.html', {'form': form, 'post': post})
    return redirect('posts:post', username=username, post_id=post.id)
