from django.shortcuts import render
from django.http import JsonResponse
from .models import Word_Set, Word

# Create your views here.
def home(request):

    return render(request, "vocab/index.html")

def set_list(request):
    word_sets = Word_Set.objects.all().order_by("set_order")

    return render(request, "vocab/word-sets.html", {"word_sets": word_sets})

def word_list(request):
    words = Word.objects.all()

    return render(request, "vocab/word-list.html", {"words": words})

def get_word_list(request):
    words = Word.objects.all()

    return JsonResponse(words)