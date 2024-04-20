from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from vocab.models import USER_UKR_ENG_META, WORD_UKR_ENG, WORD_UKR_ENG_SCORES, ALPHABET_UKR_ENG
from django.test.client import Client
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
        
