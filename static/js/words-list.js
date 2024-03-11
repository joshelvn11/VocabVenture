// Global word data variable, holds an array of word objects
let wordData;

// Get HTML elements
const wordsListTable = $("#words-list-table");

// Word Details Elements
const showDetailsButtons = $(".show-word-details-button");
const wordDetailsModal = $("#word-details-modal");
const closeWordDetailsModalButton = $("#close-word-details-modal-button");
const detailsCardContainer = $("#details-card-container");
const wordUkr = $("#word-ukr");
const wordEng = $("#word-eng");
const wordPronounce = $("#word-pronounce");
const wordRoman = $("#word-roman");
const wordExplain = $("#word-explain");

// Admin Edit Modal Elements
const adminEditButtons = $(".admin-edit-details-button");
const adminEditModal = $("#admin-edit-modal");
const closeAdminEditModalButton = $("#close-admin-edit-modal-button");
const wordIdInput = $("#word-id-input");
const wordUkrInput = $("#word-ukr-input");
const wordEngInput = $("#word-eng-input");
const wordRomanInput = $("#word-roman-input");
const wordPronounceInput = $("#word-pronounce-input");
const wordExplainInput = $("#word-explain-input");
const wordExamplesInput = $("#word-examples-input");

// Other Elements
const backgroundOverlay = $(".background-overlay");

// Add event listeners
closeWordDetailsModalButton.on("click", () => {
  closeWordDetailsModal();
});

closeAdminEditModalButton.on("click", () => {
  closeAdminEditModal();
});

showDetailsButtons.each(function () {
  $(this).on("click", function () {
    showWordDetailsModal($(this).attr("word-id"));
  });
});

adminEditButtons.each(function () {
  $(this).on("click", function () {
    showAdminEditModal($(this).attr("word-id"));
  });
});

// Fetch the word data from the api
fetch("/api/words/list")
  .then((response) => {
    if (!response.ok) {
      console.log("Error in response");
    }
    return response.json(); // Parse the response body as JSON
  })
  .then((data) => {
    wordData = data.data;
  });

function showWordDetailsModal(wordId) {
  // Find the relevant objecty from the wordData array
  const wordObject = wordData.find((obj) => obj["word_id"] == wordId);

  wordUkr.text(wordObject["word_ukrainian"]);
  wordEng.text(formatArray(wordObject["word_english"]));
  wordRoman.text(wordObject["word_roman"]);
  wordPronounce.text(wordObject["word_pronounciation"]);
  wordExplain.text(wordObject["word_explanation"]);

  loadUsageExamples(wordObject);

  // Show the modal and background overlay
  wordDetailsModal.removeClass("hidden");
  backgroundOverlay.removeClass("hidden");
}

function closeWordDetailsModal() {
  // Hide the modal and background overlay
  wordDetailsModal.addClass("hidden");
  backgroundOverlay.addClass("hidden");

  // Remove all the usage example elements
  $(".usage-example").remove();
}

function showAdminEditModal(wordId) {
  // Find the relevant objecty from the wordData array
  const wordObject = wordData.find((obj) => obj["word_id"] == wordId);

  populateAdminEditFields(wordObject);

  adminEditModal.removeClass("hidden");
  backgroundOverlay.removeClass("hidden");
}

function closeAdminEditModal() {
  // Hide the modal and background overlay
  adminEditModal.addClass("hidden");
  backgroundOverlay.addClass("hidden");
}

function loadUsageExamples(wordObject) {
  // Get the usage examples object
  usageExamplesObject = wordObject["word_examples"];

  // Iterate through the object and create an element for every example
  for (let [index, usageExample] of usageExamplesObject.entries()) {
    // Create the example element
    let exampleElement = $(`<div class="card col-12 usage-example">
        <div class="card-title">Usage Example ${index + 1}</div>
            <div class="card-content"></div>
        </div>`);

    // Create the sentence container
    let sentenceContainer = $(
      `<div class="interactive-sentence-container"></div>`
    );

    // Append each word in the example to the sentence container
    for (let [index, exampleWord] of usageExample["ukrainian"].entries()) {
      // Create the word container and insert the Ukrainian example word
      let wordContainer = $(
        `<div class="interactive-word-container"><p class="font-size-large">${exampleWord}</p></div>`
      );

      // Create the tooltip container
      let tooltipContainer = $(
        `<div class="interactive-word-tooltip-container"></div>`
      );

      // Append the tooltip container to the word container
      wordContainer.append(tooltipContainer);

      // Create the corresponding tooltips and append them to the tooltip container
      let englishTooltip = $(`<div class="interactive-word-tooltip">
                            ${usageExample["english-word-for-word"][index]}
                        </div>`);
      tooltipContainer.append(englishTooltip);
      let romanTooltip = $(`<div class="interactive-word-tooltip">
                            ${usageExample["roman-word-for-word"][index]}
                        </div>`);
      tooltipContainer.append(romanTooltip);

      // Append the word container to the sentence container
      sentenceContainer.append(wordContainer);
    }

    // Append the sentence container to the example element
    exampleElement.children(".card-content").append(sentenceContainer);

    // Create the english translation container
    let englishTranslation = $(`<div class="sentence-border-box">
    <p>Show Translation</p>
    </div>`);

    // Add event listener to translation box
    englishTranslation.on("click", () => {
      englishTranslation.children("p").text(usageExample["english"]);
    });

    // Append the english translation box to the example element
    exampleElement.children(".card-content").append(englishTranslation);

    // Append the new element to the card container
    detailsCardContainer.append(exampleElement);
  }
}

function populateAdminEditFields(wordObject) {
  wordIdInput.val(wordObject["word_id"]);
  wordUkrInput.val(wordObject["word_ukrainian"]);
  wordEngInput.val(wordObject["word_english"]);
  wordRomanInput.val(wordObject["word_roman"]);
  wordPronounceInput.val(wordObject["word_pronounciation"]);
  wordExplainInput.val(wordObject["word_explanation"]);

  wordExamplesInput.val(JSON.stringify(wordObject["word_examples"], null, 2));
}

// Function to format an array of strings into an individual string
function formatArray(arr) {
  let formattedString = "";
  for (let [index, value] of arr.entries()) {
    formattedString += value;
    // If it's not the last word in the array and a trailing comma
    if (index != arr.length - 1) {
      formattedString += ", ";
    }
  }

  return formattedString;
}
