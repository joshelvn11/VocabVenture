from django.urls import path, include
from . import views
from .views import home, set_list, word_list_ukr_eng, get_word_list
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
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
    path('api/words/list', views.get_word_list, name='get_word_list'), 
    path('api/word/list', views.getWordList, name='getWordList'), 
    path('api/words/add', views.post_word_item, name='post_word_item'), 
    path('api/words/update/<int:word_id>', views.update_word_item, name='update_word_item'), 
    path('api/words/delete/<int:word_id>', views.delete_word_item, name='delete_word_item'),
    path('api/words/sets/<int:word_id>', views.get_word_sets, name="get_word_sets"),
    path('api/words/sets/<int:set_id>/add/<int:word_id>', views.post_word_set_junction, name="post_word_set_junction"),
    path('api/words/sets/<int:set_id>/delete/<int:word_id>', views.delete_word_set_junction, name="delete_word_set_junction"),
    path('api/scores/update', views.update_user_word_score, name="update_user_word_score"),
    path('api/jobs/update-streaks', views.job_update_user_streaks, name="job_update_user_streaks"),
    path('api/user-meta/update-hint', views.update_user_meta_hint, name="update_user_meta_hint"),
    ## --------------------------------------------------------------- Missing 404 Pages
    path('<path:undefined_path>', RedirectView.as_view(url='/'), name='redirect_to_home'),
    ## --------------------------------------------------------------- PWA URLS
    #path('offline/', cache_page(settings.PWA_APP_NAME)(pwa_views.OfflineView.as_view())),
]