questionContainer = $("#practice-card-question-container");
sentenceContainer = $("#practice-card-question");
instructionText = $("#practice-card-instruction");
wordTranslation = $("#word-translation");
checkButton = $("#check-button");
wordsRemaining = $("#words-remaining");
spellingInputField = null;

// Variable to hold the index of the current question in the spelling data array
currentQuestion = 0;

// Variable to hold the current question word
currentQuestionWord = "";

checkButton.on("click", checkSpelling);

// Load the first question
loadQuestion();

function loadQuestion() {
  // Empty the container
  sentenceContainer.empty();

  // Set the number of remaining words
  wordsRemaining.text(spellingData.length - (currentQuestion + 1));

  // Load the current question sentence as an object
  currentQuestionObject = spellingData[currentQuestion];

  // Set the instruction
  wordTranslation.text(currentQuestionObject["word_eng"]);

  // Get the index of the word being questioned
  wordIndex = currentQuestionObject["word_index"];

  // Append each word in the question sentence to the sentence container
  for (let [index, word] of currentQuestionObject["sentence_ukr"].entries()) {
    // Check if the current word is the word being questioned
    if (index == wordIndex) {
      currentQuestionWord = word;

      // If it is create an input field for the question word
      spellingInputField = $(`
      <input id="spelling-input" type=text placeholder="${word}">
        `);

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
  let englishTranslation = $(`<div class="sentence-border-box">
    <p>Show Translation</p>
    </div>`);

  questionContainer.append(englishTranslation);

  // Add event listener to translation box
  englishTranslation.on("click", () => {
    englishTranslation
      .children("p")
      .text(currentQuestionObject["sentence_translation"]);
  });
}

function checkSpelling() {
  spellingInput = spellingInputField.val().toLowerCase().trim();

  if (spellingInput == currentQuestionWord.toLowerCase()) {
    showAlertModal("SUCCESS", "Correct spelling");

    currentQuestion++;

    if (currentQuestion == spellingData.length) {
      endQuiz();
    } else {
      loadQuestion();
    }
  } else {
    showAlertModal("ERROR", "INCorrect spelling");
  }
}

function endQuiz() {
  instructionText.text("Spelling set completed! 🎉");
  sentenceContainer.html(
    `<dotlottie-player id="check-lottie" src="https://lottie.host/54868f8e-d8e8-49b1-84b8-0e0973d5d8f1/UtUsM19WMG.json" background="transparent" speed="1" autoplay></dotlottie-player>`
  );
}
