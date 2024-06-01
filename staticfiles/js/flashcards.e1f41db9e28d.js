import { SCORE_INCREASE, SCORE_DECREASE, getCookie } from "./config.js";

// ------------------------------------------------------------------------- DOM Nodes

const flashcardContainer = $("#practice-card-container");
const questionFlashcard = $("#question-flashcard");
const answerFlashcard = $("#answer-flashcard");
const flashcardInstructionText = $("#practice-card-instruction");
const flashcardQuestionText = $("#practice-card-question");
const flashcardAnswerText = $("#flashcard-answer");
const incorrectButton = $("#incorrect-button");
const correctButton = $("#correct-button");
const flipCardButton = $("#flip-card-button");
const questionShowPronouncationButton = $(
  "#question-show-pronounciation-button"
);
const questionShowRomanisationButton = $(
  "#question-show-romananisation-button"
);
const questionPlayAudioButton = $("#question-play-audio-button");
const answerShowPronouncationButton = $("#answer-show-pronounciation-button");
const answerShowRomanisationButton = $("#answer-show-romananisation-button");
const answerPlayAudioButton = $("#answer-play-audio-button");
const restartButton = $("#restart-button");
const returnButton = $("#return-button");
const cardsRemaining = $("#cards-remaining");
const exitButton = $("#exit-button");

// ------------------------------------------------------------------------- Global Variables

// URL Parameters
const PARAMS = new URLSearchParams(window.location.search);

// Const to hold the practice state
const PRACTICE = PARAMS.get("practice") === "true";

// State variable to manage whether the flashcard is in its flipped state
let flipped = false;

// Array to hold the completed flash card data
let flashcardDataCompleted = [];

// Array to hold score incrementation objects
let scoreIncrements = [];

// ------------------------------------------------------------------------- Event Listeners

correctButton.on("click", () => {
  if (!PRACTICE) {
    scoreIncrements.push({
      word_id: flashcardData[0]["word_id"],
      score: flashcardData[0]["score"],
      increment_value: SCORE_INCREASE,
    });
  }

  flashcardDataCompleted.push(flashcardData.shift());

  flashcardContainer.addClass("flashing-border-green");

  if (flashcardData.length === 0) {
    endFlashcards();
  } else {
    setTimeout(setFlashcardData, 1250);
  }

  setTimeout(() => {
    flipCard();
    flashcardContainer.removeClass("flashing-border-green");
  }, 1000);
});

incorrectButton.on("click", () => {
  if (!PRACTICE) {
    scoreIncrements.push({
      word_id: flashcardData[0]["word_id"],
      score: flashcardData[0]["score"],
      increment_value: SCORE_DECREASE,
    });
    flashcardDataCompleted.push(flashcardData.shift());

    if (flashcardData.length === 0) {
      endFlashcards();
    } else {
      setTimeout(setFlashcardData, 1250);
    }
    setTimeout(() => {
      flipCard();
      flashcardContainer.removeClass("flashing-border-red");
    }, 1000);
  } else {
    flashcardData.push(flashcardData.shift());

    setTimeout(setFlashcardData, 1250);

    setTimeout(() => {
      flipCard();
      flashcardContainer.removeClass("flashing-border-red");
    }, 1000);
  }

  flashcardContainer.addClass("flashing-border-red");
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

returnButton.on("click", () => {
  window.history.back();
});

// ------------------------------------------------------------------------- Functions

function setFlashcardData() {
  if (!flashcardData || flashcardData.length === 0) {
    console.error("No flashcard data available.");
    showAlertModal("ERROR", "No flashcard data available.");
    return;
  }

  flashcardInstructionText.text(flashcardData[0]["title"]);
  flashcardQuestionText.text(flashcardData[0]["question"]);
  flashcardAnswerText.text(flashcardData[0]["answer"]);
  cardsRemaining.text(flashcardData.length);

  // Reset the button text
  questionShowRomanisationButton.text("Show Romanisation");
  // Check if the question has a romanisation property
  if ("question-roman" in flashcardData[0]) {
    // Add an event listener to show the romanisation
    questionShowRomanisationButton.on("click", () => {
      questionShowRomanisationButton.text(flashcardData[0]["question-roman"]);
    });
    // Show the romanisation button
    questionShowRomanisationButton.removeClass("hidden");
  } else {
    questionShowRomanisationButton.addClass("hidden");
  }

  // Reset the button text
  questionShowPronouncationButton.text("Show Pronounciation");
  // Check if the question has a pronounciation property
  if ("question-pronounciation" in flashcardData[0]) {
    // Add an event listener to show the pronounciation
    questionShowPronouncationButton.on("click", () => {
      questionShowPronouncationButton.text(
        flashcardData[0]["question-pronounciation"]
      );
    });
    // Show the pronounciation button
    questionShowPronouncationButton.removeClass("hidden");
  } else {
    questionShowPronouncationButton.addClass("hidden");
  }

  // Check if the question has a pronounciation audio property
  if ("question-pronounciation-audio" in flashcardData[0]) {
    // Check if the pronounciation audio has a valid extension
    if (
      flashcardData[0]["question-pronounciation-audio"].split(".").pop() ==
      "m4a"
    ) {
      // Load the pronounciation audio
      const audio = new Audio(
        flashcardData[0]["question-pronounciation-audio"]
      );

      audio.onerror = function (error) {
        console.error("Error loading audio:", error);
        showAlertModal("ERROR", "Error loading pronounciation audio");
      };

      // Remove previous event listeners
      questionPlayAudioButton.off("click");

      // Add an event listener to play the prononounciation audio
      questionPlayAudioButton.on("click", () => {
        audio.play();
      });
      // Show the pronounciation audio button
      questionPlayAudioButton.removeClass("hidden");
    } else {
      questionPlayAudioButton.addClass("hidden");
    }
  } else {
    questionPlayAudioButton.addClass("hidden");
  }

  // Reset the button text
  answerShowRomanisationButton.text("Show Romanisation");
  // Check if the answer has a romanisation property
  if ("answer-roman" in flashcardData[0]) {
    // Add an event listener to show the romanisation
    answerShowRomanisationButton.on("click", () => {
      answerShowRomanisationButton.text(flashcardData[0]["answer-roman"]);
    });
    // Show the romanisation button
    answerShowRomanisationButton.removeClass("hidden");
  } else {
    answerShowRomanisationButton.addClass("hidden");
  }

  // Reset the button text
  answerShowPronouncationButton.text("Show Pronounciation");
  // Check if the answer has a pronounciation property
  if ("answer-pronounciation" in flashcardData[0]) {
    // Add an event listener to show the pronounciation
    answerShowPronouncationButton.on("click", () => {
      answerShowPronouncationButton.text(
        flashcardData[0]["answer-pronounciation"]
      );
    });
    // Show the pronounciation button
    answerShowPronouncationButton.removeClass("hidden");
  } else {
    answerShowPronouncationButton.addClass("hidden");
  }

  // Check if the answer has a pronounciation audio property
  if ("answer-pronounciation-audio" in flashcardData[0]) {
    // Check if the pronounciation audio has a valid extension
    if (
      flashcardData[0]["answer-pronounciation-audio"].split(".").pop() == "m4a"
    ) {
      // Load the pronounciation audio
      const audio = new Audio(flashcardData[0]["answer-pronounciation-audio"]);

      audio.onerror = function (error) {
        console.error("Error loading audio:", error);
        showAlertModal("ERROR", "Error loading pronounciation audio");
      };

      // Remove previous event listeners
      answerPlayAudioButton.off("click");

      // Add an event listener to play the prononounciation audio
      answerPlayAudioButton.on("click", () => {
        audio.play();
      });
      // Show the pronounciation audio button
      answerPlayAudioButton.removeClass("hidden");
    } else {
      answerPlayAudioButton.addClass("hidden");
    }
  } else {
    answerPlayAudioButton.addClass("hidden");
  }
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
}

function endFlashcards() {
  if (!PRACTICE) {
    incrementScores();
  }
  cardsRemaining.text("0");

  flashcardInstructionText.text("Flashcard set completed! 🎉");
  setTimeout(() => {
    flashcardQuestionText.html(
      `<dotlottie-player id="check-lottie" src="https://lottie.host/54868f8e-d8e8-49b1-84b8-0e0973d5d8f1/UtUsM19WMG.json" background="transparent" speed="1" autoplay></dotlottie-player>`
    );
  }, 1000);

  // Disable the flip button
  flipCardButton.prop("disabled", true);

  // Hide buttons
  flipCardButton.addClass("hidden");
  incorrectButton.addClass("hidden");
  correctButton.addClass("hidden");
  questionShowRomanisationButton.addClass("hidden");
  questionShowPronouncationButton.addClass("hidden");
  questionPlayAudioButton.addClass("hidden");

  // Show buttons
  restartButton.removeClass("hidden");
  returnButton.removeClass("hidden");
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

function incrementScores() {
  fetch(`/api/scores/update`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      // Include CSRF token as required by Django for non-GET requests
      "X-CSRFToken": getCookie("csrftoken"),
      "Quiz-Type": 1,
    },
    body: JSON.stringify(scoreIncrements),
  });
}

// ------------------------------------------------------------------------- Starting Function

startFlashcards();
