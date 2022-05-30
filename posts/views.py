from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from typing import Dict
from .models import Post, Country


def index(request: HttpRequest) -> HttpResponse:
    template = 'posts/index.html'
    posts = Post.objects.all()[:10]
    context = {
        'posts': posts
    }
    return render(request, template, context)


def country_posts(request: HttpRequest, slug: str) -> HttpResponse:
    country = get_object_or_404(Country, slug=slug)
    posts = country.posts.all()[:10]
    templates = 'posts/country_posts.html'
    context: Dict[str, str] = {
        'country_name': slug,
        'posts': posts,
    }
    return render(request, templates, context)
