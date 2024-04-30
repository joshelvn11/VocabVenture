from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from vocab.models import USER_UKR_ENG_META, WORD_UKR_ENG, WORD_UKR_ENG_SCORES, ALPHABET_UKR_ENG, WORD_SET, SET_UKR_ENG_SCORES, WORD_SET_JUNCTION_UKR_ENG
from django.test.client import Client
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from vocab.serializers import WordUkrEngSerializer
import json

class HomeViewTests(TestCase):
    def setUp(self):
        # Create a user for the tests
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()

        word_object = WORD_UKR_ENG.objects.create(word_id=1, word_ukrainian='слово', word_english='word', word_roman='slovo', word_gender=0, word_pronounciation='slo-vo', word_pronounciation_audio='https://google.com')
        word_object.save()
        word_score = WORD_UKR_ENG_SCORES.objects.create(user=self.user, word=WORD_UKR_ENG.objects.first(), word_total_score=50)
        word_score.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/accounts/login/')  

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('home'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        # Check we used correct template
        self.assertTemplateUsed(response, 'vocab/index.html')

    def test_user_meta_creation(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('home'))
        self.assertTrue(USER_UKR_ENG_META.objects.filter(user=self.user).exists())

    def test_context_data(self):
        # Setup data
        self.client.login(username='testuser', password='12345')

        response = self.client.get(reverse('home'))
        context = response.context

        # Check if the context data is as expected
        self.assertIn('new_words', context)
        self.assertIn('learning_words', context)
        self.assertIn('learnt_words', context)
        self.assertIn('mastered_words', context)
        self.assertEqual(context['new_words'], 0)
        self.assertEqual(context['learning_words'], 1)
        self.assertEqual(context['learnt_words'], 0)
        self.assertEqual(context['mastered_words'], 0)

    def test_html_elements_in_response(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("home") + "?set=1")
        self.assertContains(response, '<p>Flashcard Current Streak</p>', html=False)

    def tearDown(self):
        # Clean up after each test
        self.user.delete()

class AlphabetListViewTests(TestCase):

    def setUp(self):
        # Create a user for the tests
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client = Client()

        # Create sample alphabet data
        sample_object = ALPHABET_UKR_ENG.objects.create(letter_id=1, 
                                        letter_ukrainian="А", 
                                        letter_explanation="sample explanation", 
                                        letter_pronounciation_audio="https://s3.eu-west-1.wasabisys.com/vocabventure/text-to-speech-letters/%D0%90.m4a",
                                        letter_examples=json.loads('{"value": null}'))
        
        sample_object.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('alphabet_list'))
        self.assertRedirects(response, '/accounts/login/')

    def test_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('alphabet_list'))

        # Check the user is logged in
        self.assertEqual(str(response.context['user']), 'testuser')
        # Check a "success" response is returned
        self.assertEqual(response.status_code, 200)
        # Check the correct template is being used
        self.assertTemplateUsed(response, 'vocab/alphabet.html')

    def test_context_data(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('alphabet_list'))

        # Check if the context data contains alphabet data
        self.assertTrue('letters' in response.context)
        # Check if the alphabet data is not empty
        self.assertTrue(response.context['letters'].exists())

    def test_html_elements_in_response(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("alphabet_list") + "?set=1")
        self.assertContains(response, '<h3 class="set-title">А</h3>', html=False)

    def tearDown(self):
        self.user.delete()

class WordSetsViewTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.user_meta = USER_UKR_ENG_META.objects.create(user=self.user)
        # Create sample WORD_SET and SET_UKR_ENG_SCORES objects
        self.word_set = WORD_SET.objects.create(set_id=1, set_order=1, set_title="Sample Set", set_slug="sample_set")
        self.set_score = SET_UKR_ENG_SCORES.objects.create(user=self.user, word_set=self.word_set, set_total_score=0, set_flashcard_eng_ukr_score=0, set_flashcard_ukr_eng_score=0, set_spelling_eng_ukr_score=0)

    def test_redirect_if_not_logged_in(self):
        # Check if the user is redirected when not logged in
        response = self.client.get(reverse('sets_list'))
        self.assertRedirects(response, '/accounts/login/')

    def test_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('sets_list'))

         # Check the user is logged in
        self.assertEqual(str(response.context['user']), 'testuser')

        # Check a success status is returned
        self.assertEqual(response.status_code, 200)

        # Check the correct template is used
        self.assertTemplateUsed(response, 'vocab/word-sets.html')

    def test_context_data(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('sets_list'))
        word_sets = response.context['word_sets']

        # Check the word_sets context data exists
        self.assertTrue(word_sets.exists())
        for word_set in word_sets:
            self.assertTrue(hasattr(word_set, 'set_total_score'))
            self.assertTrue(hasattr(word_set, 'set_total_score_color'))

    def test_html_elements_in_response(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("sets_list") + "?set=1")
        self.assertContains(response, '<h3 class="set-title">Sample Set</h3>', html=False)
        self.assertContains(response, '<p class="progress-bar-percentage">', html=False)

    def tearDown(self):
        self.user.delete()

class PracticeFlashcardsViewTests(TestCase):
    def setUp(self):
        # Create a user for the tests
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client = Client()

        # Create sample word set and words
        self.word_set = WORD_SET.objects.create(set_id=1, 
                                                set_order=1, 
                                                set_title="Sample Set", 
                                                set_slug="sample_set"
                                                )
        self.word = WORD_UKR_ENG.objects.create(word_id=1, 
                                                word_ukrainian="слово", 
                                                word_english="word", 
                                                word_roman="slovo", 
                                                word_gender=0, 
                                                word_pronounciation="slo-vo", 
                                                word_pronounciation_audio='https://google.com', 
                                                word_definition="test", 
                                                word_explanation="test", 
                                                word_part_of_speech=1,
                                                word_aspect_examples = json.loads('[{"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 1, "roman": ["Vona", "chytaty", "zhurnal"], "tense": "Present", "english": ["She", "reads", "magazine"], "cultural": "", "ukrainian": ["Вона", "читати", "журнал"], "definition": "Engaging with printed literature.", "difficulty": "Beginner", "explanation": "Used to describe the action of reading a magazine for information or entertainment.", "translation": "She is reading a magazine"}, {"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 1, "roman": ["Dity", "chytaty", "kazku"], "tense": "Present", "english": ["Children", "read", "fairy tale"], "cultural": "", "ukrainian": ["Діти", "читати", "казку"], "definition": "The act of reading a story with fantastical elements.", "difficulty": "Beginner", "explanation": "Indicates the activity of children engaging with a fairy tale, possibly as a bedtime story or for leisure.", "translation": "The children are reading a fairy tale"}, {"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 2, "roman": ["Ya", "lyublyu", "chytaty", "poeziyu"], "tense": "Present", "english": ["I", "love", "to read", "poetry"], "cultural": "", "ukrainian": ["Я", "люблю", "читати", "поезію"], "definition": "Expressing a preference for reading poetic works.", "difficulty": "Intermediate", "explanation": "Used to convey a personal enjoyment or preference for reading poetry, highlighting the emotional or aesthetic appreciation.", "translation": "I love to read poetry"}]'),
                                                word_declension = json.loads('{"value": null}'),
                                                word_conjugation = json.loads('{"value": null}'),
                                                word_examples = json.loads('{"value": null}'),
                                                )
        self.junction = WORD_SET_JUNCTION_UKR_ENG.objects.create(word_set=self.word_set, word=self.word)
        self.word.save()
        self.word_set.save()
        self.junction.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("practice_flashcards") + "?set=1")
        self.assertRedirects(response, '/accounts/login/')

    def test_flashcards_view_with_authenticated_user(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("practice_flashcards") + "?set=1")
        self.assertEqual(response.status_code, 200)
        flashcard_data = json.loads(response.context["flashcard_data"])
        self.assertTrue(isinstance(flashcard_data, list))
        self.assertEqual(len(flashcard_data), 2)  # Expecting 2 flashcards for 1 word
        self.assertIn("word_id", flashcard_data[0])
        self.assertIn("question", flashcard_data[0])
        self.assertIn("answer", flashcard_data[0])

    def test_html_elements_in_response(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("practice_flashcards") + "?set=1" + "&practice=True")
        self.assertContains(response, '<div id="practice-page">', html=False)
        self.assertContains(response, '<span id="cards-remaining">', html=False)
        self.assertContains(response, '<button id="flip-card-button" class="border-button">Flip</button>', html=False)

    def tearDown(self):
        self.user.delete()

class PracticeSpellingViewTests(TestCase):
    def setUp(self):
        # Create a user for the tests
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client = Client()        

        # Create sample word set and words
        self.word_set = WORD_SET.objects.create(set_id=1, 
                                                set_order=1, 
                                                set_title="Sample Set", 
                                                set_slug="sample_set"
                                                )
        self.word = WORD_UKR_ENG.objects.create(word_id=1, 
                                                word_ukrainian="слово", 
                                                word_english="word", 
                                                word_roman="slovo", 
                                                word_gender=0, 
                                                word_pronounciation="slo-vo", 
                                                word_pronounciation_audio='https://google.com', 
                                                word_definition="test", 
                                                word_explanation="test", 
                                                word_part_of_speech=1,
                                                word_examples = json.loads('[{"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 1, "roman": ["Vona", "chytaty", "zhurnal"], "tense": "Present", "english": ["She", "reads", "magazine"], "cultural": "", "ukrainian": ["Вона", "читати", "журнал"], "definition": "Engaging with printed literature.", "difficulty": "Beginner", "explanation": "Used to describe the action of reading a magazine for information or entertainment.", "translation": "She is reading a magazine"}, {"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 1, "roman": ["Dity", "chytaty", "kazku"], "tense": "Present", "english": ["Children", "read", "fairy tale"], "cultural": "", "ukrainian": ["Діти", "читати", "казку"], "definition": "The act of reading a story with fantastical elements.", "difficulty": "Beginner", "explanation": "Indicates the activity of children engaging with a fairy tale, possibly as a bedtime story or for leisure.", "translation": "The children are reading a fairy tale"}, {"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 2, "roman": ["Ya", "lyublyu", "chytaty", "poeziyu"], "tense": "Present", "english": ["I", "love", "to read", "poetry"], "cultural": "", "ukrainian": ["Я", "люблю", "читати", "поезію"], "definition": "Expressing a preference for reading poetic works.", "difficulty": "Intermediate", "explanation": "Used to convey a personal enjoyment or preference for reading poetry, highlighting the emotional or aesthetic appreciation.", "translation": "I love to read poetry"}]'),
                                                word_declension = json.loads('{"value": null}'),
                                                word_conjugation = json.loads('{"value": null}'),
                                                word_aspect_examples = json.loads('{"value": null}'),
                                                )
        self.junction = WORD_SET_JUNCTION_UKR_ENG.objects.create(word_set=self.word_set, word=self.word)
        self.word.save()
        self.word_set.save()
        self.junction.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("practice_spelling") + "?set=1")
        self.assertRedirects(response, "/accounts/login/")

    def test_response_with_authenticated_user(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("practice_spelling") + "?set=1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "vocab/spelling.html")

    def test_context_data(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("practice_spelling") + "?set=1")
        context = response.context
        self.assertIn("spelling_data", context)
        spelling_data = json.loads(context["spelling_data"])
        self.assertTrue(isinstance(spelling_data, list))
        self.assertGreater(len(spelling_data), 0)  # Ensure there is at least one spelling card

    def test_html_elements_in_response(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("practice_spelling") + "?set=1" + "&practice=True")
        self.assertContains(response, '<p>Words Remaining: <span id="words-remaining">null</span></p>', html=False)
        self.assertContains(response, '<button id="check-button" class="border-button">Check</button>', html=False)

    def tearDown(self):
        self.user.delete()

class GetWordListTests(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Create words and word sets
        self.word1 = WORD_UKR_ENG.objects.create(word_id=1, 
                                                word_ukrainian="UKR word 1", 
                                                word_english="ENG word 1", 
                                                word_roman="ROMAN word 1", 
                                                word_gender=0, 
                                                word_pronounciation="PRONOUNCIATION word 1", 
                                                word_pronounciation_audio='https://google.com', 
                                                word_definition="DEF 1", 
                                                word_explanation="EXP 1", 
                                                word_part_of_speech=1,
                                                word_examples = json.loads('[{"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 1, "roman": ["Vona", "chytaty", "zhurnal"], "tense": "Present", "english": ["She", "reads", "magazine"], "cultural": "", "ukrainian": ["Вона", "читати", "журнал"], "definition": "Engaging with printed literature.", "difficulty": "Beginner", "explanation": "Used to describe the action of reading a magazine for information or entertainment.", "translation": "She is reading a magazine"}, {"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 1, "roman": ["Dity", "chytaty", "kazku"], "tense": "Present", "english": ["Children", "read", "fairy tale"], "cultural": "", "ukrainian": ["Діти", "читати", "казку"], "definition": "The act of reading a story with fantastical elements.", "difficulty": "Beginner", "explanation": "Indicates the activity of children engaging with a fairy tale, possibly as a bedtime story or for leisure.", "translation": "The children are reading a fairy tale"}, {"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 2, "roman": ["Ya", "lyublyu", "chytaty", "poeziyu"], "tense": "Present", "english": ["I", "love", "to read", "poetry"], "cultural": "", "ukrainian": ["Я", "люблю", "читати", "поезію"], "definition": "Expressing a preference for reading poetic works.", "difficulty": "Intermediate", "explanation": "Used to convey a personal enjoyment or preference for reading poetry, highlighting the emotional or aesthetic appreciation.", "translation": "I love to read poetry"}]'),
                                                word_declension = json.loads('{"value": null}'),
                                                word_conjugation = json.loads('{"value": null}'),
                                                word_aspect_examples = json.loads('{"value": null}'),
                                                )
        self.word2 = WORD_UKR_ENG.objects.create(word_id=2, 
                                                word_ukrainian="UKR word 1", 
                                                word_english="ENG word 1", 
                                                word_roman="ROMAN word 1", 
                                                word_gender=0, 
                                                word_pronounciation="PRONOUNCIATION word 1", 
                                                word_pronounciation_audio='https://google.com', 
                                                word_definition="DEF 1", 
                                                word_explanation="EXP 1", 
                                                word_part_of_speech=1,
                                                word_examples = json.loads('[{"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 1, "roman": ["Vona", "chytaty", "zhurnal"], "tense": "Present", "english": ["She", "reads", "magazine"], "cultural": "", "ukrainian": ["Вона", "читати", "журнал"], "definition": "Engaging with printed literature.", "difficulty": "Beginner", "explanation": "Used to describe the action of reading a magazine for information or entertainment.", "translation": "She is reading a magazine"}, {"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 1, "roman": ["Dity", "chytaty", "kazku"], "tense": "Present", "english": ["Children", "read", "fairy tale"], "cultural": "", "ukrainian": ["Діти", "читати", "казку"], "definition": "The act of reading a story with fantastical elements.", "difficulty": "Beginner", "explanation": "Indicates the activity of children engaging with a fairy tale, possibly as a bedtime story or for leisure.", "translation": "The children are reading a fairy tale"}, {"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 2, "roman": ["Ya", "lyublyu", "chytaty", "poeziyu"], "tense": "Present", "english": ["I", "love", "to read", "poetry"], "cultural": "", "ukrainian": ["Я", "люблю", "читати", "поезію"], "definition": "Expressing a preference for reading poetic works.", "difficulty": "Intermediate", "explanation": "Used to convey a personal enjoyment or preference for reading poetry, highlighting the emotional or aesthetic appreciation.", "translation": "I love to read poetry"}]'),
                                                word_declension = json.loads('{"value": null}'),
                                                word_conjugation = json.loads('{"value": null}'),
                                                word_aspect_examples = json.loads('{"value": null}'),
                                                )
        self.word_set = WORD_SET.objects.create(set_id=1, 
                                                set_order=1, 
                                                set_title="Sample Set", 
                                                set_slug="sample_set"
                                                )
        self.junction = WORD_SET_JUNCTION_UKR_ENG.objects.create(word_set=self.word_set, word=self.word1)
        self.word1.save()
        self.word2.save()
        self.word_set.save()
        self.junction.save()
        # URL for get_word_list
        self.url = reverse('get_word_list')

    def test_request_without_set_id(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        words = WORD_UKR_ENG.objects.all()
        serializer = WordUkrEngSerializer(words, many=True)
        self.assertEqual(response.data["data"], [dict(item) for item in serializer.data])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_with_valid_set_id(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {'set-id': 1})
        words = [self.word1]
        serializer = WordUkrEngSerializer(words, many=True)
        self.assertEqual(response.data["data"], [dict(item) for item in serializer.data])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_with_invalid_set_id(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {'set-id': 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_request_with_get_scores_true_and_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        WORD_UKR_ENG_SCORES.objects.create(user=self.user, word=self.word1, word_total_score=50)
        response = self.client.get(self.url, {'get-scores': 'true'})
        self.assertIn('word_flashcard_ukr_eng_score', response.data['data'][0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        self.user.delete()

class PostWordItemTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('postWordItem') 
        self.superuser = User.objects.create_superuser('admin', 'admin@test.com', 'adminpass')
        self.user = User.objects.create_user('user', 'user@test.com', 'userpass')

    def test_access_denied_to_unauthenticated_users(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_access_denied_to_non_superuser(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_reject_invalid_data(self):
        self.client.force_authenticate(user=self.superuser)
        data = {"word_ukrainian": "", "word_english": "word"}  # Incomplete data
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_accept_valid_data(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            "word_id":1, 
            "word_ukrainian": "слово", 
            "word_english": "word", 
            "word_roman": "slovo", 
            "word_gender": 0, 
            "word_pronounciation": "slo-vo",
            "word_pronounciation_audio": 'https://google.com', 
            "word_definition": "test", 
            "word_explanation": "test", 
            "word_part_of_speech": 1,
            "word_examples": json.loads('[{"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 1, "roman": ["Vona", "chytaty", "zhurnal"], "tense": "Present", "english": ["She", "reads", "magazine"], "cultural": "", "ukrainian": ["Вона", "читати", "журнал"], "definition": "Engaging with printed literature.", "difficulty": "Beginner", "explanation": "Used to describe the action of reading a magazine for information or entertainment.", "translation": "She is reading a magazine"}, {"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 1, "roman": ["Dity", "chytaty", "kazku"], "tense": "Present", "english": ["Children", "read", "fairy tale"], "cultural": "", "ukrainian": ["Діти", "читати", "казку"], "definition": "The act of reading a story with fantastical elements.", "difficulty": "Beginner", "explanation": "Indicates the activity of children engaging with a fairy tale, possibly as a bedtime story or for leisure.", "translation": "The children are reading a fairy tale"}, {"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 2, "roman": ["Ya", "lyublyu", "chytaty", "poeziyu"], "tense": "Present", "english": ["I", "love", "to read", "poetry"], "cultural": "", "ukrainian": ["Я", "люблю", "читати", "поезію"], "definition": "Expressing a preference for reading poetic works.", "difficulty": "Intermediate", "explanation": "Used to convey a personal enjoyment or preference for reading poetry, highlighting the emotional or aesthetic appreciation.", "translation": "I love to read poetry"}]'),
            "word_declension": json.loads('{"value": null}'),
            "word_conjugation": json.loads('{"value": null}'),
            "word_aspect_examples": json.loads('{"value": null}'), 
            }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(WORD_UKR_ENG.objects.count(), 1)
    
    def test_data_saved_correctly(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            "word_id":1, 
            "word_ukrainian": "слово", 
            "word_english": "word", 
            "word_roman": "slovo", 
            "word_gender": 0, 
            "word_pronounciation": "slo-vo",
            "word_pronounciation_audio": 'https://google.com', 
            "word_definition": "test", 
            "word_explanation": "test", 
            "word_part_of_speech": 1,
            "word_examples": json.loads('[{"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 1, "roman": ["Vona", "chytaty", "zhurnal"], "tense": "Present", "english": ["She", "reads", "magazine"], "cultural": "", "ukrainian": ["Вона", "читати", "журнал"], "definition": "Engaging with printed literature.", "difficulty": "Beginner", "explanation": "Used to describe the action of reading a magazine for information or entertainment.", "translation": "She is reading a magazine"}, {"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 1, "roman": ["Dity", "chytaty", "kazku"], "tense": "Present", "english": ["Children", "read", "fairy tale"], "cultural": "", "ukrainian": ["Діти", "читати", "казку"], "definition": "The act of reading a story with fantastical elements.", "difficulty": "Beginner", "explanation": "Indicates the activity of children engaging with a fairy tale, possibly as a bedtime story or for leisure.", "translation": "The children are reading a fairy tale"}, {"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 2, "roman": ["Ya", "lyublyu", "chytaty", "poeziyu"], "tense": "Present", "english": ["I", "love", "to read", "poetry"], "cultural": "", "ukrainian": ["Я", "люблю", "читати", "поезію"], "definition": "Expressing a preference for reading poetic works.", "difficulty": "Intermediate", "explanation": "Used to convey a personal enjoyment or preference for reading poetry, highlighting the emotional or aesthetic appreciation.", "translation": "I love to read poetry"}]'),
            "word_declension": json.loads('{"value": null}'),
            "word_conjugation": json.loads('{"value": null}'),
            "word_aspect_examples": json.loads('{"value": null}'), 
            }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        word = WORD_UKR_ENG.objects.first()
        self.assertIsNotNone(word)
        self.assertEqual(word.word_ukrainian, "слово")

class UpdateWordItemTests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser("admin", "adminpass")
        self.user = User.objects.create_user("testuser", "12345")
        self.word = WORD_UKR_ENG.objects.create(word_id=1, 
                                                word_ukrainian="UKR word 1", 
                                                word_english="ENG word 1", 
                                                word_roman="ROMAN word 1", 
                                                word_gender=0, 
                                                word_pronounciation="PRONOUNCIATION word 1", 
                                                word_pronounciation_audio='https://google.com', 
                                                word_definition="DEF 1", 
                                                word_explanation="EXP 1", 
                                                word_part_of_speech=1,
                                                word_examples = json.loads('[{"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 1, "roman": ["Vona", "chytaty", "zhurnal"], "tense": "Present", "english": ["She", "reads", "magazine"], "cultural": "", "ukrainian": ["Вона", "читати", "журнал"], "definition": "Engaging with printed literature.", "difficulty": "Beginner", "explanation": "Used to describe the action of reading a magazine for information or entertainment.", "translation": "She is reading a magazine"}, {"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 1, "roman": ["Dity", "chytaty", "kazku"], "tense": "Present", "english": ["Children", "read", "fairy tale"], "cultural": "", "ukrainian": ["Діти", "читати", "казку"], "definition": "The act of reading a story with fantastical elements.", "difficulty": "Beginner", "explanation": "Indicates the activity of children engaging with a fairy tale, possibly as a bedtime story or for leisure.", "translation": "The children are reading a fairy tale"}, {"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 2, "roman": ["Ya", "lyublyu", "chytaty", "poeziyu"], "tense": "Present", "english": ["I", "love", "to read", "poetry"], "cultural": "", "ukrainian": ["Я", "люблю", "читати", "поезію"], "definition": "Expressing a preference for reading poetic works.", "difficulty": "Intermediate", "explanation": "Used to convey a personal enjoyment or preference for reading poetry, highlighting the emotional or aesthetic appreciation.", "translation": "I love to read poetry"}]'),
                                                word_declension = json.loads('{"value": null}'),
                                                word_conjugation = json.loads('{"value": null}'),
                                                word_aspect_examples = json.loads('{"value": null}'),
                                                )
        self.word.save()

        self.update_data = {
            "word_id":1, 
            "word_ukrainian": "слово", 
            "word_english": "word", 
            "word_roman": "slovo", 
            "word_gender": 0, 
            "word_pronounciation": "slo-vo",
            "word_pronounciation_audio": 'https://google.com', 
            "word_definition": "test", 
            "word_explanation": "test", 
            "word_part_of_speech": 1,
            "word_examples": json.loads('[{"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 1, "roman": ["Vona", "chytaty", "zhurnal"], "tense": "Present", "english": ["She", "reads", "magazine"], "cultural": "", "ukrainian": ["Вона", "читати", "журнал"], "definition": "Engaging with printed literature.", "difficulty": "Beginner", "explanation": "Used to describe the action of reading a magazine for information or entertainment.", "translation": "She is reading a magazine"}, {"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 1, "roman": ["Dity", "chytaty", "kazku"], "tense": "Present", "english": ["Children", "read", "fairy tale"], "cultural": "", "ukrainian": ["Діти", "читати", "казку"], "definition": "The act of reading a story with fantastical elements.", "difficulty": "Beginner", "explanation": "Indicates the activity of children engaging with a fairy tale, possibly as a bedtime story or for leisure.", "translation": "The children are reading a fairy tale"}, {"case": "Accusative", "audio": "URL_to_audio_pronunciation_of_the_sentence", "index": 2, "roman": ["Ya", "lyublyu", "chytaty", "poeziyu"], "tense": "Present", "english": ["I", "love", "to read", "poetry"], "cultural": "", "ukrainian": ["Я", "люблю", "читати", "поезію"], "definition": "Expressing a preference for reading poetic works.", "difficulty": "Intermediate", "explanation": "Used to convey a personal enjoyment or preference for reading poetry, highlighting the emotional or aesthetic appreciation.", "translation": "I love to read poetry"}]'),
            "word_declension": json.loads('{"value": null}'),
            "word_conjugation": json.loads('{"value": null}'),
            "word_aspect_examples": json.loads('{"value": null}'), 
            }
        self.url = reverse("update_word_item", kwargs={"word_id": self.word.word_id})

    def test_update_word_item_access_control(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, {"word_english": "updated_word"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.superuser)
        response = self.client.put(self.url, {"word_english": "updated_word"})
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_update_non_existent_word(self):
        self.client.force_authenticate(user=self.superuser)
        non_existent_url = reverse("update_word_item", kwargs={"word_id": 999})
        response = self.client.put(non_existent_url, {"word_english": "updated_word"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_update(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.put(self.url, self.update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.word.refresh_from_db()
        self.assertEqual(self.word.word_english, "word")
    
    def test_invalid_update(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.put(self.url, {"word_english": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def tearDown(self):
        self.user.delete()
        self.superuser.delete()
        self.word.delete()

class DeleteWordItemTests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser("admin", "adminpass")
        self.user = User.objects.create_user('user', 'user@test.com', 'userpass')
        
        # Create a sample word to be deleted
        self.word = WORD_UKR_ENG.objects.create(
            word_id=1, 
            word_ukrainian="слово", 
            word_english="word", 
            word_roman="slovo", 
            word_gender=0, 
            word_pronounciation="slo-vo",
            word_pronounciation_audio='https://google.com', 
            word_definition="definition", 
            word_explanation="explanation", 
            word_part_of_speech=1
        )
        
        # URL for deleteWordItem
        self.url = reverse("delete_word_item", kwargs={"word_id": self.word.word_id})

    def test_access_denied_to_unauthenticated_users(self):
        # Attempt to delete without authentication
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_denied_to_non_superuser(self):
        # Authenticate as a regular user
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_word_item_with_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(WORD_UKR_ENG.objects.filter(word_id=self.word.word_id).exists())

    def test_delete_non_existent_word(self):
        self.client.force_authenticate(user=self.superuser)
        non_existent_url = reverse("delete_word_item", kwargs={"word_id": 999})
        response = self.client.delete(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def tearDown(self):
        # Clean up code
        self.user.delete()
        self.superuser.delete()
        if WORD_UKR_ENG.objects.filter(word_id=self.word.word_id).exists():
            self.word.delete()

class GetWordSetsTests(APITestCase):
    def setUp(self):
        # Create a user for the tests
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create sample word and word set data
        self.word = WORD_UKR_ENG.objects.create(
            word_id=1, 
            word_ukrainian="слово", 
            word_english="word", 
            word_roman="slovo", 
            word_gender=0, 
            word_pronounciation="slo-vo",
            word_pronounciation_audio='https://google.com'
        )
        self.word_set = WORD_SET.objects.create(
            set_id = 1, 
            set_order = 1,
            set_title = "Sample Set", 
            set_slug = "sample_set"
        )
        self.junction = WORD_SET_JUNCTION_UKR_ENG.objects.create(
            word_set=self.word_set, 
            word=self.word
        )

        # URL for getWordSets
        self.url = reverse('get_word_sets', kwargs={'word_id': self.word.word_id})

    def test_get_word_sets_with_valid_word_id(self):
        response = self.client.get(self.url)
        print(response)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('data' in response.data)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['set_title'], 'Sample Set')

    def test_get_word_sets_with_invalid_word_id(self):
        # Test with a non-existent word_id
        invalid_url = reverse('get_word_sets', kwargs={'word_id': 999})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def tearDown(self):
        # Clean up code
        self.user.delete()
        self.word.delete()
        self.word_set.delete()
        self.junction.delete()