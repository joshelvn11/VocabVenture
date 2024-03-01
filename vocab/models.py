from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.


GENDER = ((0, "None"), (1, "Male"), (2, "Female"))

def default_english_words():
    return {"No Translation"}

# Model to define full list of word
class Word(models.Model):
    word_id = models.IntegerField(unique=True)
    word_ukrainian = models.CharField(max_length=100)
    word_english = ArrayField(models.CharField(max_length=50), default=default_english_words)
    word_roman = models.CharField(max_length=100)
    word_gender = models.IntegerField(choices=GENDER, default=0)
    word_pronounciation = models.CharField(max_length=100)
    word_pronounciation_audio = models.URLField(null=True)
    word_explanation = models.TextField(null=True)
    word_examples = models.JSONField(null=True)

    def __str__(self):
        return f"[ID] {self.word_id} [UKR] {self.word_ukrainian} [ENG] {self.word_english}"

# Model to define sets of words
class Word_Set(models.Model):
    set_id = models.IntegerField(unique=True)
    set_title = models.CharField(max_length=100)
    set_slug = models.SlugField(max_length=100, unique=True)
    set_order = models.IntegerField()

    def __str__(self):
        return f"[ID] {self.set_id} [TITLE] {self.set_title}"

# Junction table to define which words belong to which sets
# Junction table needed as words can belong to multiple sets 
# meaning a many-to-many relationship i.e Sets can have multiple words
# and words can have multiple sets
class Set_Word_Junction(models.Model):
    word = models.ForeignKey(Word, on_delete=models.PROTECT)
    word_set = models.ForeignKey(Word_Set, on_delete=models.PROTECT)

    class Meta:
        ordering = ["word"] 

    def __str__(self):
        return f"[WORD] {self.word} [SET] {self.word}"


