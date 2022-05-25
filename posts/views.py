from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def index(request: HttpRequest) -> HttpResponse:
    template = 'posts/index.html'
    return render(request, template)


def country_posts(request: HttpRequest, slug) -> HttpResponse:
    return HttpResponse(f'Countries posts {slug}')
