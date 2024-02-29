from django.db import models

# Create your models here.

# Model to define full list of word
class Word(models.Model):
    word_id = models.IntegerField(unique=True)
    word_ukrainian = models.CharField(max_length=100)
    word_english = models.CharField(max_length=100)
    word_roman = models.CharField(max_length=100)
    word_pronounciation = models.CharField(max_length=100)

    def __str__(self):
        return f"[ID] {self.word_id} [UKR] {self.word_ukrainian} [ENG] {self.word_english}"

# Model to define sets of words
class Word_Set(models.Model):
    set_id = models.IntegerField(unique=True)
    set_title = models.CharField(max_length=100)
    set_slug = models.SlugField(max_length=100, unique=True)

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


