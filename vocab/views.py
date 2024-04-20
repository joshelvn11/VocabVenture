from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.utils import timezone
from django.utils.timezone import now, timedelta
import json
import random
import os
import logging
from .models import WORD_SET, WORD_UKR_ENG, WORD_SET_JUNCTION_UKR_ENG, WORD_UKR_ENG_SCORES, SET_UKR_ENG_SCORES, USER_UKR_ENG_META, USER_UKR_ENG_TEST_LOG, ALPHABET_UKR_ENG
from .serializers import WordUkrEngSerializer, SetUkrEngSerializer
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Create or get a logger
logger = logging.getLogger(__name__)  

# Set log level
logger.setLevel(logging.INFO)

# Define file handler and set formatter
file_handler = logging.FileHandler('logfile.log')
formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)

# Add file handler to logger
logger.addHandler(file_handler)

## ------------------------------------------------------------------------------------------------------------------------ Template Rendering Views

def home(request):

    # Redirect the user to the login page if they are not authenticated
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    context = {}

    if request.user.is_authenticated:

        try:
            # Get the user meta object
            user_meta = USER_UKR_ENG_META.objects.get(user=request.user)
        except USER_UKR_ENG_META.DoesNotExist:
            # Create a user meta object of the user if one does not exist
            user_meta = USER_UKR_ENG_META.objects.create(
                user=request.user,
                streak_flashcards_longest=0,
                streak_flashcards_current=0,
                streak_spelling_longest=0,
                streak_spelling_current=0,
                tour_message_home_one=True,
                tour_message_word_sets_one=True,
                tour_message_word_list_one=True,
                tour_message_word_details_one=True
            )

            user_meta.save()

        # Get the streak data
        streak_flashcards_longest = user_meta.streak_flashcards_longest
        streak_flashcards_current = user_meta.streak_flashcards_current
        streak_spelling_longest = user_meta.streak_spelling_longest
        streak_spelling_current = user_meta.streak_spelling_current

        # Get the total number of words
        words_count = WORD_UKR_ENG.objects.count()

        # Retrieve all word scores for the current user
        word_scores = WORD_UKR_ENG_SCORES.objects.filter(user=request.user)
        word_scores_length = len(word_scores)

        if (word_scores_length == 0):
            word_scores_length = 1

        # Create stats for each learning stage
        new_words = len([score for score in word_scores if 0 <= score.word_total_score < 20])
        new_of_total_percent = round(((new_words / words_count) * 100), 2)
        new_of_total_bar_length = new_of_total_percent
        new_of_scored_percent = round(((new_words / word_scores_length) * 100), 2)

        learning_words = len([score for score in word_scores if 20 <= score.word_total_score < 60])
        learning_of_total_percent = round(((learning_words / words_count) * 100), 2)
        learning_of_total_bar_length = learning_of_total_percent + new_of_total_bar_length
        learning_of_scored_percent = round(((learning_words / word_scores_length) * 100), 2)

        learnt_words = len([score for score in word_scores if 60 <= score.word_total_score < 100])
        learnt_of_total_percent = round(((learnt_words / words_count) * 100), 2)
        learnt_of_total_bar_length = learnt_of_total_percent + learning_of_total_bar_length
        learnt_of_scored_percent = round(((learnt_words / word_scores_length) * 100), 2)

        mastered_words = len([score for score in word_scores if score.word_total_score == 100])
        mastered_of_total_percent = round(((mastered_words / words_count) * 100), 2)
        mastered_of_total_bar_length = mastered_of_total_percent + learnt_of_total_bar_length
        mastered_of_scored_percent = round(((mastered_words / word_scores_length) * 100), 2)

        context = {
            "streak_flashcards_longest": streak_flashcards_longest,
            "streak_flashcards_current": streak_flashcards_current,
            "streak_spelling_longest": streak_spelling_longest,
            "streak_spelling_current": streak_spelling_current,
            "new_words": new_words,
            "new_of_total_percent": new_of_total_percent,
            "new_of_scored_percent": new_of_scored_percent,
            "new_of_total_bar_length": new_of_total_bar_length,
            "learning_words": learning_words,
            "learning_of_total_percent": learning_of_total_percent,
            "learning_of_total_bar_length": learning_of_total_bar_length,
            "learning_of_scored_percent": learning_of_scored_percent,
            "learnt_words": learnt_words,
            "learnt_of_total_percent": learnt_of_total_percent,
            "learnt_of_total_bar_length": learnt_of_total_bar_length,
            "learnt_of_scored_percent": learnt_of_scored_percent,
            "mastered_words": mastered_words,
            "mastered_of_total_percent": mastered_of_total_percent,
            "mastered_of_total_bar_length": mastered_of_total_bar_length,
            "mastered_of_scored_percent": mastered_of_scored_percent,
            "user_meta": user_meta,
        }

    return render(request, "vocab/index.html", context)

def alphabet_list(request):

    # Redirect the user to the login page if they are not authenticated
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    
    alphabet = ALPHABET_UKR_ENG.objects.all()

    return render(request, "vocab/alphabet.html", alphabet)

def word_sets(request):
    """
    Renders a page of avaialble word sets ordered by the specified set_order field.
    """

    # Redirect the user to the login page if they are not authenticated
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    # Retrieve WORD_SET objects, ordered by 'set_order'
    word_sets = WORD_SET.objects.order_by("set_order")


    # Get the user meta
    user_meta = USER_UKR_ENG_META.objects.get(user=request.user)

    # Iterate over each word_set to find and append the related SET_UKR_ENG_SCORES fields
    for word_set in word_sets:
        try:
            # Attempt to find the related SET_UKR_ENG_SCORES object for the current user
            set_score = SET_UKR_ENG_SCORES.objects.get(user=request.user, word_set=word_set)
            # Manually append fields from set_score to word_set
            word_set.set_total_score = set_score.set_total_score
            word_set.set_total_score_color = get_score_color(set_score.set_total_score)
            word_set.set_flashcard_eng_ukr_score = set_score.set_flashcard_eng_ukr_score
            word_set.set_flashcard_eng_ukr_score_color = get_score_color(set_score.set_flashcard_eng_ukr_score)
            word_set.set_flashcard_ukr_eng_score = set_score.set_flashcard_ukr_eng_score
            word_set.set_flashcard_ukr_eng_score_color = get_score_color(set_score.set_flashcard_ukr_eng_score)
            word_set.set_spelling_eng_ukr_score = set_score.set_spelling_eng_ukr_score
            word_set.set_spelling_eng_ukr_score_color = get_score_color(set_score.set_spelling_eng_ukr_score)
        except SET_UKR_ENG_SCORES.DoesNotExist:
            # If no related set_score is found, you can set default values or skip
            word_set.set_total_score = 0
            word_set.set_total_score_color = get_score_color(0)
            word_set.set_flashcard_eng_ukr_score = 0
            word_set.set_flashcard_eng_ukr_score_color = get_score_color(0)
            word_set.set_flashcard_ukr_eng_score = 0
            word_set.set_flashcard_ukr_eng_score_color = get_score_color(0)
            word_set.set_spelling_eng_ukr_score = 0
            word_set.set_spelling_eng_ukr_score_color = get_score_color(0)

    return render(request, "vocab/word-sets.html", {"word_sets": word_sets, "user_meta": user_meta})

def set_list(request, set_slug):
    """
    Renders a table of words contained with the word set specified in the URL
    """

    # Redirect the user to the login page if they are not authenticated
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    # Retrieve the word set using the slug
    word_set = get_object_or_404(WORD_SET, set_slug=set_slug)

    # Query the junction table for words in the set and retrieve the word objects
    words_in_set = WORD_SET_JUNCTION_UKR_ENG.objects.filter(word_set=word_set).select_related('word')

    # Extract the WORD_UKR_ENG objects from the queryset
    words = [junction.word for junction in words_in_set]

    if request.user.is_authenticated:
    # Iterate over each word and find the relevant score
        for word in words:
            try:
                # Attempt to fetch the related word score
                word_score = WORD_UKR_ENG_SCORES.objects.get(user=request.user, word=word)
                
                # Append the score to the word object
                word.word_total_score = word_score.word_total_score
                word.word_total_score_color = get_score_color(word_score.word_total_score)
            except WORD_UKR_ENG_SCORES.DoesNotExist:
                # Set a default of zero
                word.word_total_score = 0
                word.word_total_score_color = get_score_color(0)
    
    # Get the user Meta
    try:
        user_meta = USER_UKR_ENG_META.objects.get(user=request.user)
    except USER_UKR_ENG_META.DoesNotExist:
        pass

    # Get all set objects
    sets = WORD_SET.objects.all()

    context = {'words': words, 'set_title': word_set.set_title, 'set_id': word_set.set_id, "sets": sets, "user_meta": user_meta}

    return render(request, "vocab/word-list.html", context,)

def word_list_ukr_eng(request):

    # Redirect the user to the login page if they are not authenticated
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    words =  WORD_UKR_ENG.objects.all()
    sets = WORD_SET.objects.all()

    return render(request, "vocab/word-list.html", {"words": words, "sets": sets},)

def practice_flashcards(request):

    # Redirect the user to the login page if they are not authenticated
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    
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
            "word_id": word.word_id,
            "title": "What is the meaning of this word in English",
            "question": word.word_ukrainian,
            "question-pronounciation": word.word_pronounciation,
            "question-pronounciation-audio": word.word_pronounciation_audio,
            "question-roman": word.word_roman,
            "answer": word.word_english,
            "score": "word_flashcard_ukr_eng_score",
        }

        flashcard_list.append(flashcard_ukr_to_eng)
        
        # Create the ENG to UKR flash card data
        flashcard_eng_to_ukr = {
            "word_id": word.word_id,
            "title": "What Ukrainian word has the following meaning",
            "question": word.word_english,
            "answer": word.word_ukrainian,
            "answer-pronounciation": word.word_pronounciation,
            "answer-pronounciation-audio": word.word_pronounciation_audio,
            "answer-roman": word.word_roman,
            "score": "word_flashcard_eng_ukr_score",
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

    # Redirect the user to the login page if they are not authenticated
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

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
            "word_id": word.word_id,
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

    # Get the set_id URL param
    set_id = request.GET.get('set-id', None)

    get_scores = request.GET.get('get-scores', 'false')
    
    # Convert to boolean
    get_scores = get_scores.lower() in ['true', '1', 't', 'y', 'yes']

    # Initialise variable to hold word objects
    words = None

    # Retrieve the query set
    if set_id is None:
        words = WORD_UKR_ENG.objects.all()
    else:
        word_set = get_object_or_404(WORD_SET, set_id=set_id)

        # Query the junction table for words in the set and retrieve the word objects
        words_in_set = WORD_SET_JUNCTION_UKR_ENG.objects.filter(word_set=word_set).select_related('word')

        # Extract the WORD_UKR_ENG objects from the queryset
        words = [junction.word for junction in words_in_set]

    if request.user.is_authenticated:

        # Retrieve all WORD_UKR_ENG_SCORES objects for the current user and the words retrieved above
        word_scores = WORD_UKR_ENG_SCORES.objects.filter(user=request.user, word__in=words).select_related('word')

    # Create a dictionary for sending
    data = []

    for word in words:

        # Get the user's scores for the current word if the get-scores URL param is true
        if get_scores:
            try:
                word_flashcard_ukr_eng_score = word_scores.get(word=word).word_flashcard_ukr_eng_score
                word_flashcard_eng_ukr_score = word_scores.get(word=word).word_flashcard_eng_ukr_score
                word_spelling_eng_ukr_score = word_scores.get(word=word).word_spelling_eng_ukr_score
            except WORD_UKR_ENG_SCORES.DoesNotExist:
                word_flashcard_ukr_eng_score = 0
                word_flashcard_eng_ukr_score = 0
                word_spelling_eng_ukr_score = 0
            
            # Get the score colors
            word_flashcard_ukr_eng_score_color = get_score_color(word_flashcard_ukr_eng_score)
            word_flashcard_eng_ukr_score_color = get_score_color(word_flashcard_eng_ukr_score)
            word_spelling_eng_ukr_score_color = get_score_color(word_spelling_eng_ukr_score)

        word_data = {
            "word_id": word.word_id,
            "word_ukrainian": word.word_ukrainian,
            "word_english": word.word_english,
            "word_roman": word.word_roman,
            "word_gender": word.word_gender,
            "word_part_of_speech": word.word_part_of_speech,
            "word_pronounciation": word.word_pronounciation,
            "word_pronounciation_audio": word.word_pronounciation_audio,
            "word_definition": word.word_definition,
            "word_explanation": word.word_explanation,
            "word_examples": word.word_examples,
            "word_aspect_examples": word.word_aspect_examples,
            "word_declension": word.word_declension,
            "word_conjugation": word.word_conjugation,
            "word_flashcard_ukr_eng_score": word_flashcard_ukr_eng_score,
            "word_flashcard_ukr_eng_score_color": word_flashcard_ukr_eng_score_color,
            "word_flashcard_eng_ukr_score": word_flashcard_eng_ukr_score,
            "word_flashcard_eng_ukr_score_color": word_flashcard_eng_ukr_score_color,
            "word_spelling_eng_ukr_score": word_spelling_eng_ukr_score,
            "word_spelling_eng_ukr_score_color": word_spelling_eng_ukr_score_color,
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
            word_set = WORD_SET.objects.get(set_id=set_id)
            word = WORD_UKR_ENG.objects.get(word_id=word_id)
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
            word_set = WORD_SET.objects.get(set_id=set_id)
            word = WORD_UKR_ENG.objects.get(word_id=word_id)
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

## --------------------------------------------------------------------------  UPDATE User Word Score

@api_view(["PUT"])
def updateUserWordScore(request):

    print("Updating word scores")

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get the user making the request
        user = request.user

        # Get the quiz type
        quiz_type = request.headers.get('Quiz-Type', None)
        if not quiz_type:
            return Response({"status": "ERROR", "message": "Quiz type is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Update the test log
        update_test_log(user, int(quiz_type))

        # Convert the request body to a Python dictionary
        try:
            request_data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({"status": "ERROR", "message": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a list of Word Sets to be updated
        set_list = []

        # Iterate over the score update objects
        for score_data in request_data:
            word_id = score_data.get("word_id")
            score = score_data.get("score")
            increment_value = int(score_data.get("increment_value"))

            try:
                # Retrieve the word object using the provided word_id
                word = WORD_UKR_ENG.objects.get(word_id=word_id)
                # Retrieve the word score object for the user and word, or create a new one if it doesn't exist
                word_score, created = WORD_UKR_ENG_SCORES.objects.get_or_create(user=user, word=word, defaults={score: increment_value})
                
                # Retrieve all set junctions for the current word
                set_junctions = WORD_SET_JUNCTION_UKR_ENG.objects.filter(word=word)
                # Extract the set objects from the junctions
                sets_for_word = [junction.word_set for junction in set_junctions]
                # Add the sets to the set_list
                set_list.extend(sets_for_word)

                if not created:
                    # If the word score object already exists, update the score
                    match score:
                        case "word_flashcard_eng_ukr_score":
                            word_score.word_flashcard_eng_ukr_score += increment_value
                            if word_score.word_flashcard_eng_ukr_score > 100:
                                word_score.word_flashcard_eng_ukr_score = 100
                            if word_score.word_flashcard_eng_ukr_score < 0:
                                word_score.word_flashcard_eng_ukr_score = 0
                            word_score.save()
                        case "word_flashcard_ukr_eng_score":
                            word_score.word_flashcard_ukr_eng_score += increment_value
                            if word_score.word_flashcard_ukr_eng_score > 100:
                                word_score.word_flashcard_ukr_eng_score = 100
                            if word_score.word_flashcard_ukr_eng_score < 0:
                                word_score.word_flashcard_ukr_eng_score = 0
                            word_score.save()
                        case "word_spelling_eng_ukr_score":
                            word_score.word_spelling_eng_ukr_score += increment_value
                            if word_score.word_spelling_eng_ukr_score > 100:
                                word_score.word_spelling_eng_ukr_score = 100
                            if word_score.word_spelling_eng_ukr_score < 0:
                                word_score.word_spelling_eng_ukr_score = 0
                            word_score.save()
                
                # Update the word total score
                word_score.word_total_score = (word_score.word_flashcard_eng_ukr_score + word_score.word_flashcard_ukr_eng_score + word_score.word_spelling_eng_ukr_score) / 3
                word_score.save()

                # Convert the list to a set to get rid of duplicate objects
                word_sets = set(set_list)
                # Update the set scores
                update_set_scores(word_sets, user)
                
            except WORD_UKR_ENG.DoesNotExist:
                return Response({"status": "ERROR", "message": "Word not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                print(e)
                return Response({"status": "ERROR", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"status": "SUCCESS", "message": "Word score updated successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "ERROR", "message": "Unauthorized: Only logged in can perform this action"}, status=status.HTTP_403_FORBIDDEN)

## --------------------------------------------------------------------------  GET Update User Streaks [JOB]

@api_view(["GET"])
def job_update_user_streaks(request):

    try:
        # Log a message
        logger.info("Starting the job to update user streaks.")

        # Fetch the job_secret_key from environment variables
        job_secret_key = os.environ.get('JOB_SECRET_KEY')

        # Fetch the secret_key from the query parameters
        query_secret_key = request.query_params.get('secret_key')

        # Check if the secret key is valid
        if query_secret_key is None:
            return Response({"status": "ERROR", "message": "Missing secret_key in query parameters"}, status=status.HTTP_400_BAD_REQUEST)
        elif query_secret_key != job_secret_key:
            return Response({"status": "ERROR", "message": "Incorrect secret key value in query parameters"}, status=status.HTTP_400_BAD_REQUEST)

        # Get all user meta data objects
        user_meta = USER_UKR_ENG_META.objects.all()

        # Calculate yesterday's date
        yesterday = now() - timedelta(days=1)

        # Get all test logs for the previous day
        test_logs = USER_UKR_ENG_TEST_LOG.objects.filter(test_date=yesterday.date())

        # Loop through the list of user meta and check if they took a test yesterday
        for user_meta_object in user_meta:
            user_test_logs = test_logs.filter(user=user_meta_object.user)

            flashcards_tested = False
            spelling_tested = False

            # Loop through their test logs an update the tested bools
            for user_test_log in user_test_logs:
                if user_test_log.quiz_type == 0:
                    spelling_tested = True
                elif user_test_log.quiz_type == 1:
                    flashcards_tested = True
            
            # Update their streak to 0 if they did not take a test
            if not spelling_tested:
                user_meta_object.streak_spelling_current = 0
            
            if not flashcards_tested:
                user_meta_object.streak_flashcards_current = 0

            # Save the user meta object
            user_meta_object.save()

        # After all operations are successfully completed, return a success HTTP response
        return Response({"status": "SUCCESS", "message": "Streaks and scores updated successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"An error occurred while updating user streaks: {str(e)}")
        return Response({"status": "ERROR", "message": "An error occurred while processing the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

## --------------------------------------------------------------------------  PATCH Update User Meta Hints

@api_view(["GET"])
def update_user_meta_hint(request):

    if request.user.is_authenticated:
        # Get the set_id URL param
        hint_id = request.GET.get('hint-id', None)

        # Get the user meta object for the current user
        user_meta = USER_UKR_ENG_META.objects.get(user=request.user)

        # Return an error if the url is missing the hint id parameter
        if hint_id is None:
            return Response({"status": "ERROR", "message": "Missing hint-id paramter"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the relevant user hint status
        if hint_id == "tour_message_home_one":
            user_meta.tour_message_home_one = False
        elif hint_id == "tour_message_word_sets_one":
            user_meta.tour_message_word_sets_one = False
        elif hint_id == "tour_message_word_list_one":
            user_meta.tour_message_word_list_one = False
        elif hint_id == "tour_message_word_details_one":
            user_meta.tour_message_word_details_one = False
        elif hint_id == "tour_message_quiz_one":
            user_meta.tour_message_quiz_one = False
        else:
            # Return an error if the id is not recognized
            return Response({"status": "ERROR", "message": "Hint id not recognized"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_meta.save()
        return Response({"status": "SUCCESS", "message": "Updated hint status successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "ERROR", "message": "User must be logged in to update hint status"}, status=status.HTTP_401_UNAUTHORIZED)

def update_set_scores(word_sets, user):

    # Convert word sets to set type if it is not already a set
    if not isinstance(word_sets, set):
        word_sets = set(word_sets)

    for word_set in word_sets:
        # Retrieve all word objects that are part of the current word_set
        words_in_set = WORD_SET_JUNCTION_UKR_ENG.objects.filter(word_set=word_set).select_related('word')

        # Extract the word IDs from the queryset
        word_ids = [junction.word.id for junction in words_in_set]

        # Retrieve the word_score objects for the words in the current set that match the current user
        word_scores_in_set = WORD_UKR_ENG_SCORES.objects.filter(word_id__in=word_ids, user=user)
        # Get the set length
        set_length = len(words_in_set)

        # Iterate over the word_scores_in_set to get score totals
        set_flashcard_eng_ukr_score = 0
        set_flashcard_ukr_eng_score = 0
        set_spelling_eng_ukr_score = 0

        for word_score in word_scores_in_set:
            set_flashcard_eng_ukr_score += word_score.word_flashcard_eng_ukr_score
            set_flashcard_ukr_eng_score += word_score.word_flashcard_ukr_eng_score
            set_spelling_eng_ukr_score += word_score.word_spelling_eng_ukr_score

        # Divide each score by the set_length to get the average score
        set_flashcard_eng_ukr_score = set_flashcard_eng_ukr_score / set_length
        set_flashcard_ukr_eng_score = set_flashcard_ukr_eng_score / set_length
        set_spelling_eng_ukr_score = set_spelling_eng_ukr_score / set_length

        # Get the total average score
        set_total_score = (set_flashcard_eng_ukr_score + set_flashcard_ukr_eng_score + set_spelling_eng_ukr_score) / 3

        # Set the set score values
        try:
            # Attempt to retrieve the SET_UKR_ENG_SCORES object for the current word_set
            set_scores = SET_UKR_ENG_SCORES.objects.get(word_set=word_set, user=user)
        except SET_UKR_ENG_SCORES.DoesNotExist:
            # If the SET_UKR_ENG_SCORES object does not exist, create a new one
            set_scores = SET_UKR_ENG_SCORES.objects.create(
                user=user,
                word_set=word_set,
                set_total_score=0,
                set_flashcard_eng_ukr_score=0,
                set_flashcard_ukr_eng_score=0,
                set_spelling_eng_ukr_score=0
            )

        # Update the scores with the calculated values
        set_scores.set_flashcard_eng_ukr_score = set_flashcard_eng_ukr_score
        set_scores.set_flashcard_ukr_eng_score = set_flashcard_ukr_eng_score
        set_scores.set_spelling_eng_ukr_score = set_spelling_eng_ukr_score
        set_scores.set_total_score = set_total_score
        set_scores.save()

def update_test_log(user, quiz_type):
    
    # Get today's date in the appropriate format
    today_date = timezone.now().date()

    # Check if an entry matching today's date, the quiz type and requesting user exist
    test_log_exists = USER_UKR_ENG_TEST_LOG.objects.filter(user=user, quiz_type=quiz_type, test_date=today_date).exists()

    # If the entry does not exist, create a new one
    if not test_log_exists:

        # Find the related USER_META object
        user_meta = USER_UKR_ENG_META.objects.get(user=user)

        test_log = USER_UKR_ENG_TEST_LOG.objects.create(
            user=user,
            user_meta=user_meta,
            quiz_type=quiz_type
        )
        test_log.save()
        print(f"New test log entry created for user: {user.username}, quiz type: {quiz_type}")
        
        # Update the user's streak
        update_streak(user, quiz_type)
    else:
        print(f"Test log entry already exists for user: {user.username}, quiz type: {quiz_type}")

def update_streak(user, quiz_type):
    # Initialize the streak counter
    streak_count = 0

    # Get all test_log entries for the user and quiz type, ordered by date in descending order
    test_logs = USER_UKR_ENG_TEST_LOG.objects.filter(user=user, quiz_type=quiz_type).order_by('-test_date')

    # Check if there are any test logs
    if test_logs.exists():
        # Get the most recent test log's date
        last_date = test_logs.first().test_date

        # Iterate through the test logs to count the streak
        for log in test_logs:
            # Calculate the difference in days between the last date and the current log's date
            delta = (last_date - log.test_date).days

            # If the difference is 1, it means the streak continues
            if delta == 1:
                streak_count += 1
                # Update the last_date to the current log's date
                last_date = log.test_date
            # If the difference is 0, it means it's the same day, so set the streak to 1 day
            elif delta == 0:
                streak_count = 1
            # If the difference is more than 1, the streak breaks
            else:
                break

    # Update the user's streak in the USER_UKR_ENG_META model
    user_meta, created = USER_UKR_ENG_META.objects.get_or_create(user=user)
    if quiz_type == 1: 
        user_meta.streak_flashcards_current = streak_count
        # Check if the current streak is the longest streak
        if streak_count > user_meta.streak_flashcards_longest:
            user_meta.streak_flashcards_longest = streak_count
    elif quiz_type == 0: 
        user_meta.streak_spelling_current = streak_count
        # Check if the current streak is the longest streak
        if streak_count > user_meta.streak_spelling_longest:
            user_meta.streak_spelling_longest = streak_count
    user_meta.save()

    print(f"Updated streak for user: {user.username}, quiz type: {quiz_type}, current streak: {streak_count}")

def get_score_color(score):

    if score < 25:
        return "red"
    elif score >= 25 and score < 75:
        return "orange"
    elif score >= 75 and score < 100:
        return "green"
    elif score == 100:
        return "purple"
    
