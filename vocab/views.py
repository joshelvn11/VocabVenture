from django.shortcuts import render
from .models import Word_Set

# Create your views here.
def set_list(request):
    word_sets = Word_Set.objects.all().order_by("set_order")

    return render(request, "vocab/word-sets.html", {"word_sets": word_sets})
