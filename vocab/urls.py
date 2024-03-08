from django.urls import path
from .views import home, set_list, word_list_ukr_eng, get_word_list

urlpatterns = [
    path('', home, name='home'),
    path('words/sets', set_list, name='sets_list'), 
    path('words/list', word_list_ukr_eng, name='word_list'), 
    # API URLS
    path('api/words/list', get_word_list, name='get_word_list'), 
]