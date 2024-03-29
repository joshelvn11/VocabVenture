from django.urls import path
from . import views
from .views import home, set_list, word_list_ukr_eng, get_word_list

urlpatterns = [
    path('', home, name='home'),
    ## --------------------------------------------------------------- Words URLS
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
    path('api/words/update/<int:word_id>', views.updateWordItem, name='updateWordItem'), 
    path('api/words/delete/<int:word_id>', views.deleteWordItem, name='deleteWordItem'),
    path('api/words/sets/<int:word_id>', views.getWordSets, name="getWordSets"),
    path('api/words/sets/<int:set_id>/add/<int:word_id>', views.postWordSetJunction, name="postWordSetJunction"),
    path('api/words/sets/<int:set_id>/delete/<int:word_id>', views.deleteWordSetJunction, name="deleteWordSetJunction"),
    # path('api/words/sets/add'),
    # path('api/words/sets/update'),  
   ## path('api/words/<int:word_id>', WordUkrEngUpdateView.as_view(), name='word_update'), 
]