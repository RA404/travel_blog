from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest
from typing import Dict
from .models import Post, Country, User
from .forms import PostForm


def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    context = {
        'page_posts': page_posts,
    }
    template = 'posts/index.html'

    return render(request, template, context)


def country_posts(request: HttpRequest, slug: str) -> HttpResponse:
    country = get_object_or_404(Country, slug=slug)
    posts = country.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    context: Dict[str, str] = {
        'country': country,
        'page_posts': page_posts,
    }
    templates = 'posts/country_posts.html'

    return render(request, templates, context)


def profile(request: HttpRequest, user_name: str) -> HttpResponse:
    user = get_object_or_404(User, username=user_name)
    posts = Post.objects.filter(author=user)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    context = {
        'page_posts': page_posts,
        'author': user,
        'posts': posts,
    }

    templates = 'posts/profile.html'

    return render(request, templates, context)


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=post_id)

    context = {
        'post': post,
    }

    templates = 'posts/post_detail.html'

    return render(request, templates, context)


@login_required(login_url='users:login')
def post_create(request: HttpRequest) -> HttpResponse:
    form = PostForm(request.POST or None)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()

        return redirect('travel_posts:profile', request.user)

    return render(request, 'posts/create_post.html', {'form': form})


@login_required(login_url='users:login')
def post_edit(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('travel_posts:main')

    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()

        return redirect('travel_posts:post_detail', post_id)

    return render(
        request,
        'posts/update_post.html',
        {'form': form, 'post': post}
    )
