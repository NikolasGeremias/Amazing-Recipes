# from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('Home 1')


def contato(request):
    return HttpResponse('contato')


def sobre(request):
    return HttpResponse('sobre')
