from rest_framework import serializers
import logging
from .models import WORD_UKR_ENG, WORD_SET

# Configure logger for the application
logger = logging.getLogger(__name__)


class WordUkrEngSerializer(serializers.ModelSerializer):
    class Meta:
        model = WORD_UKR_ENG
        fields = "__all__"


class SetUkrEngSerializer(serializers.ModelSerializer):
    class Meta:
        model = WORD_SET
        fields = "__all__"
