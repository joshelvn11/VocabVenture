from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import ALPHABET_UKR_ENG, WORD_UKR_ENG, WORD_SET, WORD_SET_JUNCTION_UKR_ENG, WORD_UKR_ENG_SCORES, SET_UKR_ENG_SCORES, USER_UKR_ENG_META, USER_UKR_ENG_TEST_LOG

# Register your models here.
admin.site.register(ALPHABET_UKR_ENG)
admin.site.register(WORD_UKR_ENG)
admin.site.register(WORD_SET)
admin.site.register(WORD_SET_JUNCTION_UKR_ENG)
admin.site.register(WORD_UKR_ENG_SCORES)
admin.site.register(SET_UKR_ENG_SCORES)
admin.site.register(USER_UKR_ENG_META)
admin.site.register(USER_UKR_ENG_TEST_LOG)
