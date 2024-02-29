from django.core.management.base import BaseCommand
from django.core.serializers import serialize
from vocab.models import Word  # Import your model

class Command(BaseCommand):
    help = 'Export data as JSON'

    def handle(self, *args, **kwargs):
        data = serialize('json', Word.objects.all())
        self.stdout.write(data)