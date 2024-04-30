from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

GENDER = ((0, "None"), (1, "Male"), (2, "Female"))
PART_OF_SPEECH = ((0, "Noun"), (1, "Verb"), (2, "Adjective"), (3, "Adverb"), (4, "Pronoun"), (5, "Numeral"), (6, "Preposition"), (7, "Conjunction"), (8, "Interjection"), (9, "Particle"))
QUIZ_TYPE = ((0, "SPELLING"), (1, "FLASHCARD"))

def default_english_words():
    return {"No Translation"}

class ALPHABET_UKR_ENG(models.Model):
    letter_id = models.IntegerField(unique=True)
    letter_ukrainian = models.CharField(max_length=100)
    letter_explanation = models.CharField(max_length=100)
    letter_pronounciation_audio = models.URLField(null=True)
    letter_examples = models.JSONField(null=True, editable=True)

    class Meta:
        verbose_name = "Letter (UKR/ENG)"
        verbose_name_plural = "Alphabet (UKR/ENG)"

    def __str__(self): 
        return f"[ID] {self.letter_id} [UKR] {self.letter_ukrainian}"

# Model to define full list of word
class WORD_UKR_ENG(models.Model):
    word_id = models.IntegerField(unique=True)
    word_ukrainian = models.CharField(max_length=100)
    word_english = models.CharField(max_length=100)
    word_roman = models.CharField(max_length=100)
    word_gender = models.IntegerField(choices=GENDER, default=0)
    word_pronounciation = models.CharField(max_length=100)
    word_pronounciation_audio = models.URLField(null=True)
    word_definition = models.TextField(null=True)
    word_explanation = models.TextField(null=True)
    word_part_of_speech = models.IntegerField(choices=PART_OF_SPEECH, default=0)
    word_aspect_examples = models.JSONField(null=True, editable=True)
    word_declension = models.JSONField(null=True, editable=True)
    word_conjugation = models.JSONField(null=True, editable=True)
    word_examples = models.JSONField(null=True, editable=True)

    class Meta:
        verbose_name = "Word (UKR/ENG)"
        verbose_name_plural = "Words (UKR/ENG)"

    def __str__(self):
        return f"[ID] {self.word_id} [UKR] {self.word_ukrainian} [ENG] {self.word_english}"

# Model to define sets of words
class WORD_SET(models.Model):
    set_id = models.IntegerField(unique=True)
    set_title = models.CharField(max_length=100)
    set_slug = models.SlugField(max_length=100, unique=True)
    set_order = models.IntegerField()

    class Meta:
        verbose_name = "Set (UKR/ENG)"
        verbose_name_plural = "Sets (UKR/ENG)"

    def __str__(self):
        return f"[ID] {self.set_id} [TITLE] {self.set_title}"

# Junction table to define which words belong to which sets
# Junction table needed as words can belong to multiple sets 
# meaning a many-to-many relationship i.e Sets can have multiple words
# and words can have multiple sets
class WORD_SET_JUNCTION_UKR_ENG(models.Model):
    word = models.ForeignKey(WORD_UKR_ENG, on_delete=models.CASCADE)
    word_set = models.ForeignKey(WORD_SET, on_delete=models.PROTECT)

    class Meta:
        ordering = ["word"]
        verbose_name = "Word/Set Junction(UKR/ENG)"
        verbose_name_plural = "Word/Set Junctions (UKR/ENG)" 

    def __str__(self):
        return f"[WORD] {self.word} [SET] {self.word}"

# Model to hold Word UKR-ENG user scores
class WORD_UKR_ENG_SCORES(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_word_scores')
    word = models.ForeignKey(WORD_UKR_ENG, on_delete=models.CASCADE, related_name='word_scores')
    word_total_score = models.IntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ])
    word_flashcard_eng_ukr_score = models.IntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ])
    word_flashcard_ukr_eng_score = models.IntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ])
    word_spelling_eng_ukr_score = models.IntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ])

    class Meta:
        unique_together = ('user', 'word')  # Ensures that each user-word pair is unique
        verbose_name = "Word Score (UKR/ENG)"
        verbose_name_plural = "Word Scores (UKR/ENG)"

    def __str__(self):
        return f"[User] {self.user.username} [Word] {self. word.word_ukrainian}"
    
# Model to hold set scores
class SET_UKR_ENG_SCORES(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_set_scores')
    word_set = models.ForeignKey(WORD_SET, on_delete=models.CASCADE, related_name='set_scores')
    set_total_score = models.IntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ])
    set_flashcard_eng_ukr_score = models.IntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ])
    set_flashcard_ukr_eng_score = models.IntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ])
    set_spelling_eng_ukr_score = models.IntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ])

    class Meta:
        verbose_name = "Set Score (UKR/ENG)"
        verbose_name_plural = "Set Scores (UKR/ENG)"

    def __str__(self):
        return f"[User] {self.user.username} [SET] {self.word_set}"


class USER_UKR_ENG_META(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_meta_user')
    streak_flashcards_longest = models.IntegerField(default=0)
    streak_flashcards_current = models.IntegerField(default=0)
    streak_spelling_longest = models.IntegerField(default=0)
    streak_spelling_current = models.IntegerField(default=0)
    tour_message_home_one = models.BooleanField(default=True)
    tour_message_alphabet_one = models.BooleanField(default=True)
    tour_message_word_sets_one = models.BooleanField(default=True)
    tour_message_word_list_one = models.BooleanField(default=True)
    tour_message_word_details_one = models.BooleanField(default=True)
    tour_message_quiz_one = models.BooleanField(default=True)

    class Meta:
        verbose_name = "User Meta"
        verbose_name_plural = "User Meta Data"

    def __str__(self):
        return f"[User] {self.user.username}"
    
class USER_UKR_ENG_TEST_LOG(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_log_user')
    user_meta = models.ForeignKey(USER_UKR_ENG_META, on_delete=models.CASCADE, related_name='user_ukr_eng_meta')
    test_date = models.DateField(auto_now_add=True)
    quiz_type = models.IntegerField(choices=QUIZ_TYPE, default=0)

    class Meta:
        verbose_name = "User Test Log Record"
        verbose_name_plural = "User Test Log Records"

    def __str__(self):
        return f"[User] {self.user.username} [DATE] {self.test_date}"
