
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import json
import random
from .models import WORD_SET, WORD_UKR_ENG, WORD_SET_JUNCTION_UKR_ENG
from .serializers import WordUkrEngSerializer, SetUkrEngSerializer

## ------------------------------------------------------------------------------------------------------------------------ Template Rendering Views

def home(request):

    return render(request, "vocab/index.html")

def word_sets(request):
    """
    Renders a page of avaialble word sets ordered by the specified set_order field.
    """
    word_sets = WORD_SET.objects.all().order_by("set_order")

    return render(request, "vocab/word-sets.html", {"word_sets": word_sets})


def set_list(request, set_slug):
    """
    Renders a table of words contained with the word set specified in the URL
    """

    # Retrieve the word set using the slug
    word_set = get_object_or_404(WORD_SET, set_slug=set_slug)

    # Query the junction table for words in the set and retrieve the word objects
    words_in_set = WORD_SET_JUNCTION_UKR_ENG.objects.filter(word_set=word_set).select_related('word')

    # Extract the WORD_UKR_ENG objects from the queryset
    words = [junction.word for junction in words_in_set]

    # Get all set objects
    sets = WORD_SET.objects.all()

    context = {'words': words, 'set_title': word_set.set_title, 'set_id': word_set.set_id, "sets": sets}

    return render(request, "vocab/word-list.html", context,)

def word_list_ukr_eng(request):
    words =  WORD_UKR_ENG.objects.all()
    sets = WORD_SET.objects.all()

    return render(request, "vocab/word-list.html", {"words": words, "sets": sets},)

def practice_flashcards(request):
    
    # Get the set pass a URL paramater
    set_param = request.GET.get('set', '1')

    # Retrieve the word set using the slug
    word_set = get_object_or_404(WORD_SET, set_id=set_param)

    # Query the junction table for words in the set and retrieve the word objects
    words_in_set = WORD_SET_JUNCTION_UKR_ENG.objects.filter(word_set=word_set).select_related('word')

    # Extract the WORD_UKR_ENG objects from the queryset
    words = [junction.word for junction in words_in_set]

    # Create list to hold flash cards
    flashcard_list = []

    # Iterate through the words an create a flashcard dict. for each
    for word in words:

        # Create the UKR to ENG flash card data
        flashcard_ukr_to_eng = {
            "title": "What is the meaning of this word in English",
            "question": word.word_ukrainian,
            "question-pronounciation": word.word_pronounciation,
            "question-pronounciation-audio": word.word_pronounciation_audio,
            "question-roman": word.word_roman,
            "answer": word.word_english,
        }

        flashcard_list.append(flashcard_ukr_to_eng)
        
        # Create the ENG to UKR flash card data
        flashcard_eng_to_ukr = {
            "title": "What Ukrainian word has the following meaning",
            "question": word.word_english,
            "answer": word.word_ukrainian,
            "answer-pronounciation": word.word_pronounciation,
            "answer-pronounciation-audio": word.word_pronounciation_audio,
            "answer-roman": word.word_roman,
        }

        # Append it to the flash card array
        flashcard_list.append(flashcard_eng_to_ukr)

    # Shuffle the flashcard list
    random.shuffle(flashcard_list)

    # Convert it to JSON
    flashcard_data = json.dumps(flashcard_list)

    # Create context
    context = {"page_title": word_set.set_title, "flashcard_data": flashcard_data}

    # Render template using context
    return render(request, "vocab/flashcards.html", context)

def practice_spelling(request):

    # Get the set pass a URL paramater
    set_param = request.GET.get('set', '1')

    # Retrieve the word set using the slug
    word_set = get_object_or_404(WORD_SET, set_id=set_param)

    # Query the junction table for words in the set and retrieve the word objects
    words_in_set = WORD_SET_JUNCTION_UKR_ENG.objects.filter(word_set=word_set).select_related('word')

    # Extract the WORD_UKR_ENG objects from the queryset
    words = [junction.word for junction in words_in_set]

    # Create list to hold spelling cards
    spellingcards_list = []

    # Iterate through the words an create a spellingcard dict. for each
    for word in words:

        # Get a random usage example as a dictionary
        usage_example = word.word_examples[random.randint(0, (len(word.word_examples) - 1))]


        spellingcard = {
            "word_ukr": word.word_ukrainian,
            "word_eng": word.word_english,
            "sentence_ukr": usage_example["ukrainian"],
            "word_index": usage_example["index"],
            "sentence_eng": usage_example["english"],
            "sentence_roman": usage_example["roman"],
            "sentence_translation": usage_example["translation"],
            "pronounciation_audio": word.word_pronounciation_audio,
        }

        spellingcards_list.append(spellingcard)

    # Shuffle the list
    random.shuffle(spellingcards_list)
    
    # Convert the card to JSON
    spellingcard_data = json.dumps(spellingcards_list)

    # Create the context
    context = {"page_title": word_set.set_title, "spelling_data": spellingcard_data}

    return render(request, "vocab/spelling.html", context)

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

    # Check if the user is authenticated and is a superuser
    if request.user.is_authenticated and request.user.is_superuser:
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
    else:
        # If the user is not a superuser, return an unauthorized error response
        return Response({"status": "ERROR",
                         "message": "Unauthorized: Only superusers can perform this action"},
                        status=status.HTTP_403_FORBIDDEN)
    
## --------------------------------------------------------------------------  PUT Word Item

@api_view(["PUT"])
def updateWordItem(request, word_id):
    # Check if the user is authenticated and is a superuser
    if request.user.is_authenticated and request.user.is_superuser:
        print("Received word item POST request")
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
    else:
        # If the user is not a superuser, return an unauthorized error response
        return Response({"status": "ERROR",
                         "message": "Unauthorized: Only superusers can perform this action"},
                        status=status.HTTP_403_FORBIDDEN)


## --------------------------------------------------------------------------  DELETE Word Item

@api_view(["DELETE"])
def deleteWordItem(request, word_id):
     # Check if the user is authenticated and is a superuser
    if request.user.is_authenticated and request.user.is_superuser:
        try:
            # Retrieve the existing word item by id
            word_item = WORD_UKR_ENG.objects.get(word_id=word_id)
        except WORD_UKR_ENG.DoesNotExist:
            # If the word item does not exist, return a 404 Not Found response
            return Response({"status": "ERROR", "message": "Word not found"}, status=status.HTTP_404_NOT_FOUND)

        # Delete the found word item
        word_item.delete()

        # Return a success response
        return Response({"status": "SUCCESS", "message": "Word deleted successfully"})
    else:
        # If the user is not a superuser, return an unauthorized error response
        return Response({"status": "ERROR",
                         "message": "Unauthorized: Only superusers can perform this action"},
                        status=status.HTTP_403_FORBIDDEN)


## --------------------------------------------------------------------------  GET Word Sets

@api_view(["GET"])
def getWordSets(request, word_id):
    # Get the specified word object
    word = WORD_UKR_ENG.objects.get(word_id=word_id)
    
    # Use the junction table to find the corresponding sets for the word
    word_sets = WORD_SET.objects.filter(word_set_junction_ukr_eng__word=word)
    
    # Serialize the items for the response
    serializer = SetUkrEngSerializer(word_sets, many=True)

    # Return the serialized data
    return Response(serializer.data)

## --------------------------------------------------------------------------  POST Word Set Junction

@api_view(["POST"])
def postWordSetJunction(request, set_id, word_id):

    # Check if the user is authenticated and is a superuser
    if request.user.is_authenticated and request.user.is_superuser:
        print("Received word set junction POST request")

        try:
            # Retrieve the word and set objects using the provided IDs from the params
            word_set = WORD_SET.objects.get(set_id=set_id);
            word = WORD_UKR_ENG.objects.get(word_id=word_id);
        except WORD_SET.DoesNotExist:
            return Response({"status": "ERROR", "message": "Set not found"}, status=status.HTTP_404_NOT_FOUND)
        except WORD_UKR_ENG.DoesNotExist:
            return Response({"status": "ERROR", "message": "Word not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create a new junction table record
        new_junction = WORD_SET_JUNCTION_UKR_ENG(word_set=word_set, word=word)
        new_junction.save()

        return Response({"status": "SUCCESS", "message": "Word added to set successfully"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"status": "ERROR", "message": "Unauthorized: Only superusers can perform this action"}, status=status.HTTP_403_FORBIDDEN)

## --------------------------------------------------------------------------  DELETE Word Set Junction

@api_view(["DELETE"])
def deleteWordSetJunction(request, set_id, word_id):

    # Check if the user is authenticated and is a superuser
    if request.user.is_authenticated and request.user.is_superuser:
        print("Received word set junction DELETE request")

        try:
            # Retrieve the word and set objects using the provided IDs from the params
            word_set = WORD_SET.objects.get(set_id=set_id);
            word = WORD_UKR_ENG.objects.get(word_id=word_id);
        except WORD_SET.DoesNotExist:
            return Response({"status": "ERROR", "message": "Set not found"}, status=status.HTTP_404_NOT_FOUND)
        except WORD_UKR_ENG.DoesNotExist:
            return Response({"status": "ERROR", "message": "Word not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create a new junction table record
        junction = WORD_SET_JUNCTION_UKR_ENG.objects.get(word=word, word_set=word_set)
        junction.delete()

        return Response({"status": "SUCCESS", "message": "Word removed from set successfully"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"status": "ERROR", "message": "Unauthorized: Only superusers can perform this action"}, status=status.HTTP_403_FORBIDDEN)

