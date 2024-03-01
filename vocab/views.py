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
    # Retrieve the query set
    words = Word.objects.all()

    # Create a dictionary for sending
    data = []

    for word in words:
        word_data = {
            "word_ukrainian": word.word_ukrainian,
            "word_english": word.word_english,
            "word_roman": word.word_roman,
            "word_gender": word.word_gender,
            "word_pronounciation": word.word_pronounciation,
            "word_explanation": word.word_explanation,
            "word_examples": word.word_examples,
        }

        data.append(word_data)

    data_response = {
        "message": "Success!",
        "data": data,
    }

    return JsonResponse(data_response)