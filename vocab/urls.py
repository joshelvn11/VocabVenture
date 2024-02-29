from django.urls import path
from .views import set_list

urlpatterns = [
    path('vocab-sets/', set_list, name='sets_list'),  # Map the view to a URL
]