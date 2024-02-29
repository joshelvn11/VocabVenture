from django.urls import path
from .views import home, set_list

urlpatterns = [
    path('', home, name='home'),
    path('vocab-sets/', set_list, name='sets_list'), 
]