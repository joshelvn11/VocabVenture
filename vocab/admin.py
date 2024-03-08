from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import WORD_UKR_ENG, WORD_SET, WORD_SET_JUNCTION_UKR_ENG

# Register your models here.
admin.site.register(WORD_UKR_ENG)
admin.site.register(WORD_SET)
admin.site.register(WORD_SET_JUNCTION_UKR_ENG)
