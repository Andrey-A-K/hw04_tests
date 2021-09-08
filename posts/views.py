from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Group
from .forms import PostForm, CommentForm

User = get_user_model()


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'posts/index.html',
                  {'page': page,
                   'post_list': post_list})


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
    form = PostForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:posts_index')
    form = PostForm()
    return render(request, 'posts/new_post.html', {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    author_posts = author.posts.all().order_by('-pub_date')
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
    post = get_object_or_404(author.posts, id=post_id)
    comments = post.comments.all()
    image = post.image
    posts_count = Post.objects.filter(author=author).count()
    form = CommentForm()
    context = {
        'form': form,
        'image': image,
        'comments': comments,
        'author': author,
        'post': post,
        'posts_count': posts_count,
        'post_id': post_id,
    }
    return render(request, 'post.html', context)


@login_required
def post_edit(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile)
    if request.user != profile:
        return redirect('posts:post', username=username, post_id=post_id)
    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=post)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('posts:post',
                            username=request.user.username,
                            post_id=post_id)

    return render(
        request, 'new_post.html', {'form': form, 'post': post},
    )


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


def add_comment(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post', username, post_id)
