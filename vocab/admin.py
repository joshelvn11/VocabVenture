from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Word, Word_Set, Set_Word_Junction

# Register your models here.
admin.site.register(Word)
admin.site.register(Word_Set)
admin.site.register(Set_Word_Junction)
