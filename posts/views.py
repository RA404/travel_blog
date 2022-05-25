from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Main page')


def country_posts(request: HttpRequest, slug) -> HttpResponse:
    return HttpResponse(f'Countries posts {slug}')
