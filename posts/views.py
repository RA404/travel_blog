from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('Main page')


def country_posts(request):
    return HttpResponse('Countries posts')
