import { SCORE_INCREASE, SCORE_DECREASE, getCookie } from "./config.js";
// ------------------------------------------------------------------------- DOM Nodes

const spellingCard = $("#practice-card-container");
const questionContainer = $("#practice-card-question-container");
const sentenceContainer = $("#practice-card-question");
const instructionText = $("#practice-card-instruction");
const wordTranslation = $("#word-translation");
const checkButton = $("#check-button");
const wordsRemaining = $("#words-remaining");
const returnButton = $("#return-button");
const exitButton = $("#exit-button");
let spellingInputField;
let englishTranslation;

// ------------------------------------------------------------------------- Global Variables

// URL Parameters
const PARAMS = new URLSearchParams(window.location.search);

// Const to hold the practice state
const PRACTICE = PARAMS.get("practice") === "true";

// Variable to hold the index of the current question in the spelling data array
let currentQuestion = 0;

// Variable to hold the current question word
let currentQuestionWord = "";

// Array to hold score incrementation objects
let scoreIncrements = [];

// ------------------------------------------------------------------------- Event Listeners

checkButton.on("click", checkSpelling);

exitButton.on("click", () => {
  window.history.back();
});

returnButton.on("click", () => {
  window.history.back();
});

// ------------------------------------------------------------------------- Functions

function loadQuestion() {
  // Empty the container
  sentenceContainer.empty();

  // Set the number of remaining words
  wordsRemaining.text(spellingData.length - (currentQuestion + 1));

  // Load the current question sentence as an object
  let currentQuestionObject = spellingData[currentQuestion];

  // Set the instruction
  wordTranslation.text(currentQuestionObject["word_eng"]);

  // Get the index of the word being questioned
  const wordIndex = currentQuestionObject["word_index"];

  // Append each word in the question sentence to the sentence container
  for (let [index, word] of currentQuestionObject["sentence_ukr"].entries()) {
    // Check if the current word is the word being questioned
    if (index == wordIndex) {
      currentQuestionWord = word;

      // Removing trailing punctuation
      let lastChar = currentQuestionWord.charAt(currentQuestionWord.length - 1);
      if (
        lastChar === "!" ||
        lastChar === "," ||
        lastChar === ":" ||
        lastChar === "?"
      ) {
        currentQuestionWord = currentQuestionWord.slice(0, -1);
      }

      // If it is create an input field for the question word
      spellingInputField = $(`
      <input id="spelling-input" type=text placeholder="${
        PRACTICE ? currentQuestionWord : ""
      }">
        `);

      spellingInputField.keypress(function (event) {
        // Check spelling when enter is pressed
        if (event.which == 13 || event.keyCode == 13) {
          checkSpelling();
        }
      });

      spellingInputField.focus();

      // Create a temporary span to measure the text width
      const tempSpan = $("<span>")
        .text(word)
        .css({
          position: "absolute", // Position absolutely to avoid affecting layout
          visibility: "hidden", // Make it invisible
          "white-space": "pre", // Preserve spaces and line breaks like in an input
          "font-family": spellingInputField.css("font-family"), // Match font properties
          "font-size": spellingInputField.css("font-size"),
          "font-weight": spellingInputField.css("font-weight"),
          "letter-spacing": spellingInputField.css("letter-spacing"),
        });

      // Append it to the body to measure its width
      $("body").append(tempSpan);
      const textWidth = tempSpan.width();
      tempSpan.remove();

      spellingInputField.width(textWidth + 8);

      sentenceContainer.append(spellingInputField);

      if (
        lastChar === "!" ||
        lastChar === "," ||
        lastChar === ":" ||
        lastChar === "?"
      ) {
        //sentenceContainer.append(lastChar);
      }
    } else {
      // Create the word container and insert the Ukrainian example word
      let wordContainer = $(
        `<div class="interactive-word-container"><p class="font-size-large">${word}</p></div>`
      );

      // Create the tooltip container
      let tooltipContainer = $(
        `<div class="interactive-word-tooltip-container"></div>`
      );

      // Append the tooltip container to the word container
      wordContainer.append(tooltipContainer);

      // Create the corresponding tooltips and append them to the tooltip container
      let englishTooltip = $(`<div class="interactive-word-tooltip">
                                ${currentQuestionObject["sentence_eng"][index]}
                            </div>`);
      tooltipContainer.append(englishTooltip);
      let romanTooltip = $(`<div class="interactive-word-tooltip">
                                ${currentQuestionObject["sentence_roman"][index]}
                            </div>`);
      tooltipContainer.append(romanTooltip);

      // Append the word container to the sentence container
      sentenceContainer.append(wordContainer);
    }
  }

  // Create the english translation container
  englishTranslation = $(`<div class="sentence-border-box">
    <p>Show Translation</p>
    </div>`);

  questionContainer.append(englishTranslation);

  // Add event listener to translation box
  englishTranslation.on("click", () => {
    englishTranslation
      .children("p")
      .text(currentQuestionObject["sentence_translation"]);
  });

  // Add focus to the input field
  spellingInputField.focus();
}

function checkSpelling() {
  let spellingInput = spellingInputField.val().toLowerCase().trim();

  if (spellingInput == currentQuestionWord.toLowerCase()) {
    // If in test mode append the score increment to the score increments array
    if (!PRACTICE) {
      scoreIncrements.push({
        word_id: spellingData[currentQuestion]["word_id"],
        score: "word_spelling_eng_ukr_score",
        increment_value: SCORE_INCREASE,
      });
    }

    currentQuestion++;

    if (currentQuestion == spellingData.length) {
      spellingCard.addClass("flashing-border-green");
      setTimeout(() => {
        spellingCard.removeClass("flashing-border-green");
        englishTranslation.remove();
        endQuiz();
      }, 1000);
    } else {
      spellingCard.addClass("flashing-border-green");
      setTimeout(() => {
        spellingCard.removeClass("flashing-border-green");
        englishTranslation.remove();
        loadQuestion();
      }, 1000);
    }
  } else {
    spellingCard.addClass("flashing-border-red");

    if (PRACTICE) {
      setTimeout(() => {
        spellingCard.removeClass("flashing-border-red");
        spellingInputField.val("");
      }, 1000);
    } else {
      scoreIncrements.push({
        word_id: spellingData[currentQuestion]["word_id"],
        score: "word_spelling_eng_ukr_score",
        increment_value: SCORE_DECREASE,
      });
      currentQuestion++;
      if (currentQuestion == spellingData.length) {
        setTimeout(() => {
          spellingCard.removeClass("flashing-border-red");
          englishTranslation.remove();
          endQuiz();
        }, 1000);
      } else {
        setTimeout(() => {
          spellingCard.removeClass("flashing-border-red");
          englishTranslation.remove();
          loadQuestion();
        }, 1000);
      }
    }
  }
}

function endQuiz() {
  checkButton.remove();

  instructionText.text("Spelling set completed! 🎉");
  sentenceContainer.html(
    `<dotlottie-player id="check-lottie" src="https://lottie.host/54868f8e-d8e8-49b1-84b8-0e0973d5d8f1/UtUsM19WMG.json" background="transparent" speed="1" autoplay></dotlottie-player>`
  );
  incrementScores();
}

function incrementScores() {
  fetch(`/api/scores/update`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      // Include CSRF token as required by Django for non-GET requests
      "X-CSRFToken": getCookie("csrftoken"),
      "Quiz-Type": 0,
    },
    body: JSON.stringify(scoreIncrements),
  });
}

// ------------------------------------------------------------------------- Script Start

// Load the first question
loadQuestion();
