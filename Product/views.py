from django.shortcuts import render
from django.utils.translation import get_language
from django.views.decorators.cache import cache_page


@cache_page(60 * 15)
def start(request):
    current_language = get_language()
    return render(request, 'start.html', {'LANGUAGE_CODE': current_language})


@cache_page(60 * 15)
def suspects(request):
    current_language = get_language()
    return render(request, 'suspects.html', {'LANGUAGE_CODE': current_language})


@cache_page(60 * 15)
def interrogation(request):
    current_language = get_language()
    return render(request, 'interrogation.html', {'LANGUAGE_CODE': current_language})


@cache_page(60 * 15)
def result(request):
    current_language = get_language()
    return render(request, 'result.html', {'LANGUAGE_CODE': current_language})
