from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils.translation import get_language, get_language_bidi


@cache_page(60 * 15)
def start(request):
    current_language = get_language()
    is_bidi = get_language_bidi()

    return render(request, 'start.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
    })


@cache_page(60 * 15)
def suspects(request):
    current_language = get_language()
    is_bidi = get_language_bidi()

    return render(request, 'suspects.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
    })


@cache_page(60 * 15)
def interrogation(request):
    current_language = get_language()
    is_bidi = get_language_bidi()

    return render(request, 'interrogation.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
    })


@cache_page(60 * 15)
def evidence(request):
    current_language = get_language()
    is_bidi = get_language_bidi()

    return render(request, 'evidence.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
    })


@cache_page(60 * 15)
def result(request):
    current_language = get_language()
    is_bidi = get_language_bidi()

    return render(request, 'result.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
    })


@cache_page(60 * 15)
def autopsy(request):
    current_language = get_language()
    is_bidi = get_language_bidi()

    return render(request, 'autopsy.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
    })
