flashcardContainer = $("#flashcard-container");
questionFlashcard = $("#question-flashcard");
answerFlashcard = $("#answer-flashcard");
flashcardInstructionText = $("#flashcard-instruction");
flashcardQuestionText = $("#flashcard-question");
flashcardAnswerText = $("#flashcard-answer");
incorrectButton = $("#incorrect-button");
correctButton = $("#correct-button");
flipCardButton = $("#flip-card-button");
restartButton = $("#restart-button");
returnButton = $("#return-button");
testButton = $("#test-button");
cardsRemaining = $("#cards-remaining");
exitButton = $("#exit-button");

// State variable to manage whether the flashcard is in its flipped state
flipped = false;

// Array to hold the completed flash card data
flashcardDataCompleted = [];

startFlashcards();

correctButton.on("click", () => {
  flashcardDataCompleted.push(flashcardData.shift());

  if (flashcardData.length === 0) {
    endFlashcards();
  } else {
    setTimeout(setFlashcardData, 250);
  }

  flipCard();
});

incorrectButton.on("click", () => {
  flashcardData.push(flashcardData.shift());
  flipCard();
  setTimeout(setFlashcardData, 250);
});

flipCardButton.on("click", () => {
  flipCard();
});

exitButton.on("click", () => {
  window.history.back();
});

restartButton.on("click", () => {
  startFlashcards(true);
});

function setFlashcardData() {
  flashcardInstructionText.text(flashcardData[0]["title"]);
  flashcardQuestionText.text(flashcardData[0]["question"]);
  flashcardAnswerText.text(flashcardData[0]["answer"]);
  cardsRemaining.text(flashcardData.length);
}

function startFlashcards(restart = false) {
  if (restart) {
    // Add all the completed flash cards onto the current flash cards array
    flashcardData.push(...flashcardDataCompleted);
  }

  setFlashcardData();
  enableAnswerButtons(false);

  // Show buttons
  flipCardButton.removeClass("hidden");
  flipCardButton.prop("disabled", false);
  incorrectButton.removeClass("hidden");
  correctButton.removeClass("hidden");

  // Show buttons
  restartButton.addClass("hidden");
  returnButton.addClass("hidden");
  testButton.addClass("hidden");
}

function endFlashcards() {
  flashcardInstructionText.text("Flashcard set completed! 🎉");
  flashcardQuestionText.text("Well done!");

  // Disable the flip button
  flipCardButton.prop("disabled", true);

  // Hide buttons
  flipCardButton.addClass("hidden");
  incorrectButton.addClass("hidden");
  correctButton.addClass("hidden");

  // Show buttons
  restartButton.removeClass("hidden");
  returnButton.removeClass("hidden");
  testButton.removeClass("hidden");
}

function flipCard() {
  // Invert the flipped state
  flipped = !flipped;
  // Toggle the flipped classes trigerring the flipping animations
  questionFlashcard.toggleClass("flipped");
  answerFlashcard.toggleClass("flipped");

  enableAnswerButtons(flipped);
}

function enableAnswerButtons(enable) {
  correctButton.prop("disabled", !enable);
  incorrectButton.prop("disabled", !enable);

  if (enable) {
    correctButton.removeClass("disabled");
    incorrectButton.removeClass("disabled");
  } else if (!enable) {
    correctButton.addClass("disabled");
    incorrectButton.addClass("disabled");
  }
}
