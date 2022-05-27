from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from typing import Dict


def index(request: HttpRequest) -> HttpResponse:
    template = 'posts/index.html'
    return render(request, template)


def country_posts(request: HttpRequest, slug) -> HttpResponse:
    templates = 'posts/country_posts.html'
    context: Dict[str, str] = {
        'country_name': slug,
    }
    return render(request, templates, context)
