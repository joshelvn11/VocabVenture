
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import json
from .models import WORD_SET, WORD_UKR_ENG, WORD_SET_JUNCTION_UKR_ENG
from .serializers import WordUkrEngSerializer

## ------------------------------------------------------------------------------------------------------------------------ Template Rendering Views

def home(request):

    return render(request, "vocab/index.html")

def set_list(request):
    word_sets = WORD_SET.objects.all().order_by("set_order")

    return render(request, "vocab/word-sets.html", {"word_sets": word_sets})

def word_list_ukr_eng(request):
    words =  WORD_UKR_ENG.objects.all()

    return render(request, "vocab/word-list.html", {"words": words},)

## ------------------------------------------------------------------------------------------------------------------------ API Views

## --------------------------------------------------------------------------  GET Word List 

def get_word_list(request):
    # Retrieve the query set
    words = WORD_UKR_ENG.objects.all()

    # Create a dictionary for sending
    data = []

    for word in words:
        word_data = {
            "word_id": word.word_id,
            "word_ukrainian": word.word_ukrainian,
            "word_english": word.word_english,
            "word_roman": word.word_roman,
            "word_gender": word.word_gender,
            "word_pronounciation": word.word_pronounciation,
            "word_pronounciation_audio": word.word_pronounciation_audio,
            "word_explanation": word.word_explanation,
            "word_examples": word.word_examples,
        }

        data.append(word_data)

    data_response = {
        "message": "Success!",
        "data": data,
    }

    return JsonResponse(data_response)

## --------------------------------------------------------------------------  GET Word List

@api_view(["GET"])
def getWordList(request):
    # Retrieve the query set
    words = WORD_UKR_ENG.objects.all()

    # Serialize the items for the response
    serializer = WordUkrEngSerializer(words, many=True)

    # Return the serialized data
    return Response(serializer.data)

## --------------------------------------------------------------------------  POST Word Item

@api_view(["POST"])
def postWordItem(request):

    print("Received word item POST request")

    # Serialize the received post data
    serializer = WordUkrEngSerializer(data=request.data)

    # Check if the serialized data is valid
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "SUCCESS",
                         "message": "Word added successfully"})
    else:
         return Response({"status": "ERROR",
                         "message": json.dumps(serializer.errors)})
    
## --------------------------------------------------------------------------  PUT Word Item

@api_view(["PUT"])
def updateWordItem(request, word_id):
    try:
        # Retrieve the existing word item by id
        word_item = WORD_UKR_ENG.objects.get(word_id=word_id)
    except WORD_UKR_ENG.DoesNotExist:
        # If the word item does not exist, return a 404 Not Found response
        return Response({"status": "ERROR",
                         "message": "Word not found"})

    # Serialize the incoming data with the existing word item instance
    serializer = WordUkrEngSerializer(word_item, data=request.data)

    # Check if the serialized data is valid
    if serializer.is_valid():
        # Save the updated word item
        serializer.save()
        # Return the updated word item data
        return Response({"status": "SUCCESS",
                         "message": "Word updated successfully"})
    else:
        # If data is invalid, return the errors
        return Response({"status": "ERROR",
                         "message": json.dumps(serializer.errors)})
    


