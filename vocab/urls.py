from django.urls import path, include
from . import views
from .views import home, set_list, word_list_ukr_eng, get_word_list
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.conf.urls.static import static
from pwa import views as pwa_views

urlpatterns = [
    path('', home, name='home'),
    path('', include('pwa.urls')),
    ## --------------------------------------------------------------- Words URLS
    path('alphabet', views.alphabet_list, name='alphabet_list'), 
    path('words/sets', views.word_sets, name='sets_list'), 
    path('words/sets/<slug:set_slug>', views.set_list, name='set_detail'),
    path('words/list', word_list_ukr_eng, name='word_list'),
    ## --------------------------------------------------------------- Practice URLS
    path('practice/flashcards', views.practice_flashcards, name='practice_flashcards'),
    path('practice/spelling', views.practice_spelling, name='practice_spelling'),
    ## --------------------------------------------------------------- API URLS
    path('api/words/list', get_word_list, name='get_word_list'), 
    path('api/word/list', views.getWordList, name='getWordList'), 
    path('api/words/add', views.postWordItem, name='postWordItem'), 
    path('api/words/update/<int:word_id>', views.updateWordItem, name='update_word_item'), 
    path('api/words/delete/<int:word_id>', views.deleteWordItem, name='delete_word_item'),
    path('api/words/sets/<int:word_id>', views.getWordSets, name="get_word_sets"),
    path('api/words/sets/<int:set_id>/add/<int:word_id>', views.postWordSetJunction, name="postWordSetJunction"),
    path('api/words/sets/<int:set_id>/delete/<int:word_id>', views.deleteWordSetJunction, name="deleteWordSetJunction"),
    path('api/scores/update', views.updateUserWordScore, name="updateUserWordScore"),
    path('api/jobs/update-streaks', views.job_update_user_streaks, name="job_update_user_streaks"),
    path('api/user-meta/update-hint', views.update_user_meta_hint, name="update_user_meta_hint"),
    ## --------------------------------------------------------------- PWA URLS
    #path('offline/', cache_page(settings.PWA_APP_NAME)(pwa_views.OfflineView.as_view())),
]