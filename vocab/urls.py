from django.urls import path
from . import views
from .views import home, set_list, word_list_ukr_eng, get_word_list

urlpatterns = [
    path('', home, name='home'),
    ## --------------------------------------------------------------- Words URLS
    path('words/sets', set_list, name='sets_list'), 
    path('words/list', word_list_ukr_eng, name='word_list'), 
    ## --------------------------------------------------------------- API URLS
    path('api/words/list', get_word_list, name='get_word_list'), 
    path('api/word/list', views.getWordList, name='getWordList'), 
    path('api/words/add', views.postWordItem, name='postWordItem'), 
    path('api/words/update/<int:word_id>', views.updateWordItem, name='updateWordItem'), 
    path('api/words/delete/<int:word_id>', views.deleteWordItem, name='deleteWordItem'), 
   ## path('api/words/<int:word_id>', WordUkrEngUpdateView.as_view(), name='word_update'), 
]