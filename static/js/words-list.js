// Global word data variable, holds an array of word objects
let wordData;
let editWordID; // Word that is currently beind edited in the admin from
let editAction = "NONE"; // State variable to control whether a word is being added or updated

// ------------------------------------------------------------------------- DOM Elements

// Get HTML elements
const wordsListTable = $("#words-list-table");

// Word Details Elements
const wordCards = $(".word-card");
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
const adminEditButton = $(".admin-edit-details-button");
const addWordButton = $("#add-word-button");
const adminEditModal = $("#admin-edit-modal");
const closeAdminEditModalButton = $("#close-admin-edit-modal-button");
const adminEditForm = $("#admin-word-edit-form");
const adminEditFormSaveButton = $("#admin-word-edit-save-button");
const adminEditFormDeleteButton = $("#admin-word-edit-delete-button");
const wordIdInput = $("#word-id-input");
const wordUkrInput = $("#word-ukr-input");
const wordEngInput = $("#word-eng-input");
const wordRomanInput = $("#word-roman-input");
const wordGenderInput = $("#word-gender-input");
const wordPronounceInput = $("#word-pronounce-input");
const wordPronounceAudioInput = $("#word-pronounce-audio-input");
const wordExplainInput = $("#word-explain-input");
const wordExamplesInput = $("#word-examples-input");
const setCheckBoxes = $(".set-checkbox");

// Other Elements
const backgroundOverlay = $(".background-overlay");

// ------------------------------------------------------------------------- Event Listeners

closeWordDetailsModalButton.on("click", () => {
  closeWordDetailsModal();
});

closeAdminEditModalButton.on("click", () => {
  closeAdminEditModal();
});

adminEditFormSaveButton.on("click", () => {
  console.log("saving word");
  submitWordEditUpdate();
});

adminEditFormDeleteButton.on("click", () => {
  editAction = "DELETE";
  let confirmDetele = confirm(
    "Are you sure you want to delete this word? This action cannot be undone"
  );
  if (confirmDetele) {
    submitWordEditUpdate();
  }
});

wordCards.each(function () {
  $(this).on("click", function () {
    showWordDetailsModal($(this).attr("word-id"));
  });
});

adminEditButton.on("click", function () {
  editAction = "UPDATE";
  closeWordDetailsModal();
  showAdminEditModal($(this).attr("word-id"));
});

addWordButton.on("click", () => {
  editAction = "ADD";
  showAdminEditModal();
});

setCheckBoxes.each(function () {
  $(this).on("change", function () {
    // Check if the checkbox is being checked or unchecked
    if ($(this).prop("checked")) {
      // If it is being checked and set word junction
      addDeleteSet($(this).attr("set-id"), true);
    } else {
      // If it is being unchecked remove a set word junction
      addDeleteSet($(this).attr("set-id"), false);
    }
  });
});

// ------------------------------------------------------------------------- FETCH Word Data

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
    console.log("Loaded word data from API");
  });

// ------------------------------------------------------------------------- User Modal Functions

function showWordDetailsModal(wordId) {
  // Find the relevant objecty from the wordData array
  const wordObject = wordData.find((obj) => obj["word_id"] == wordId);
  console.log(wordObject);
  wordUkr.text(wordObject["word_ukrainian"]);
  wordEng.text(wordObject["word_english"]);
  wordRoman.text(wordObject["word_roman"]);
  wordPronounce.text(wordObject["word_pronounciation"]);
  wordExplain.text(wordObject["word_explanation"]);

  // Load usage examples
  loadUsageExamples(wordObject);

  // Set the word id of the admin edit button
  adminEditButton.attr("word-id", wordId);

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

function loadUsageExamples(wordObject) {
  // Get the usage examples object
  usageExamplesObject = wordObject["word_examples"];

  // Iterate through the object and create an element for every example
  for (let [index, usageExample] of usageExamplesObject.entries()) {
    // Create the example element
    let exampleElement = $(`
      <div class="card word-detail-card align-center justify-center usage-example">
        <div class="card-content">
          <div class="card-title">Usage Example ${index + 1}</div>
          <div class="usage-example-container"></div>
        </div>
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
    exampleElement.find(".usage-example-container").append(sentenceContainer);

    // Create the english translation container
    let englishTranslation = $(`<div class="sentence-border-box">
    <p>Show Translation</p>
    </div>`);

    // Add event listener to translation box
    englishTranslation.on("click", () => {
      englishTranslation.children("p").text(usageExample["english"]);
    });

    // Append the english translation box to the example element
    exampleElement.find(".usage-example-container").append(englishTranslation);

    // Append the new element to the card container
    detailsCardContainer.append(exampleElement);
  }
}

// ------------------------------------------------------------------------- Admin Modal Functions

function showAdminEditModal(wordId) {
  // Populate the fields with word data if is editinng words
  if (editAction === "UPDATE") {
    // Find the relevant objecty from the wordData array
    editWordID = wordId;
    const wordObject = wordData.find((obj) => obj["word_id"] == wordId);

    populateAdminEditFields(wordObject);
    populateSetCheckBoxes(wordId);
  }

  adminEditModal.removeClass("hidden");
  backgroundOverlay.removeClass("hidden");
}

function closeAdminEditModal() {
  // Hide the modal and background overlay
  adminEditModal.addClass("hidden");
  backgroundOverlay.addClass("hidden");
}

function populateAdminEditFields(wordObject) {
  // Load the data into all the form fields
  wordIdInput.val(wordObject["word_id"]);
  wordUkrInput.val(wordObject["word_ukrainian"]);
  wordEngInput.val(wordObject["word_english"]);
  wordRomanInput.val(wordObject["word_roman"]);
  wordGenderInput.val(wordObject["word_gender"]);
  wordPronounceInput.val(wordObject["word_pronounciation"]);
  wordPronounceAudioInput.val(wordObject["word_pronounciation_audio"]);
  wordExplainInput.val(wordObject["word_explanation"]);
  wordExamplesInput.val(JSON.stringify(wordObject["word_examples"], null, 2));
}

function populateSetCheckBoxes(wordId) {
  fetch(`http://127.0.0.1:8000/api/words/sets/${wordId}`, {
    method: "GET",
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      // Iterate over the list of sets
      data.forEach((setObject) => {
        // Find the matching check box and set it to checked
        setCheckBoxes
          .filter(function () {
            return $(this).attr("set-id") == setObject["set_id"];
          })
          .prop("checked", true);
      });
    });
}

function submitWordEditUpdate() {
  // Get the form data object
  const formData = new FormData(
    document.getElementById("admin-word-edit-form")
  );

  // Parse the word examples to JSON
  wordExamples = {};
  try {
    wordExamples = JSON.parse(formData.get("word_examples"));
  } catch (error) {
    showAlertModal("ERROR", `Error in usage examples syntax (${error})`);
    console.log(`Error in usage examples syntax (${error})`);
  }

  // Convert the form data to JSON
  const jsonData = {
    word_id: Number(formData.get("word_id")),
    word_ukrainian: formData.get("word_ukrainian"),
    word_english: formData.get("word_english"),
    word_roman: formData.get("word_roman"),
    word_gender: Number(formData.get("word_gender")),
    word_pronounciation: formData.get("word_pronounciation"),
    word_pronounciation_audio: formData.get("word_pronounciation_audio"),
    word_explanation: formData.get("word_explanation"),
    word_examples: wordExamples,
  };

  if (editAction === "UPDATE") {
    // Logic to run if updating a word record
    fetch(`https://vocabventure.onrender.com/api/words/update/${editWordID}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        // Include CSRF token as required by Django for non-GET requests
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify(jsonData),
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        showAlertModal(data.status, data.message);
      });
  } else if (editAction === "ADD") {
    // Logic to run if adding a word record
    fetch(`https://vocabventure.onrender.com/api/words/add`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // Include CSRF token as required by Django for non-GET requests
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify(jsonData),
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log(data);
        showAlertModal(data.status, data.message);
      });
  } else if (editAction === "DELETE") {
    // Logic to running if deleting a word record
    fetch(`https://vocabventure.onrender.com/api/words/delete/${editWordID}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        // Include CSRF token as required by Django for non-GET requests
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log(data);
        showAlertModal(data.status, data.message);
      });
  }
}

function addDeleteSet(setId, addSet) {
  if (addSet) {
    fetch(`http://127.0.0.1:8000/api/words/sets/${setId}/add/${editWordID}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // Include CSRF token as required by Django for non-GET requests
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log(data);
      });
  } else {
    fetch(
      `http://127.0.0.1:8000/api/words/sets/${setId}/delete/${editWordID}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          // Include CSRF token as required by Django for non-GET requests
          "X-CSRFToken": getCookie("csrftoken"),
        },
      }
    )
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log(data);
      });
  }
}

// ------------------------------------------------------------------------- Utility Functions

// Function to get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
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
