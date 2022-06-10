from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from typing import Dict
from .models import Post, Country, User


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
        'country_name': slug,
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
