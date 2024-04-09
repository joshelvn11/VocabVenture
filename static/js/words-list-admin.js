// ------------------------------------------------------------------------- DOM Elements

const adminEditButton = $("#admin-edit-details-button");
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
const wordPartOfSpeechInput = $("#word-pos-input");
const wordDefinitionInput = $("#word-definition-input");
const wordExplainInput = $("#word-explain-input");
const wordExamplesInput = $("#word-examples-input");
const wordAspectInput = $("#word-aspect-input");
const wordDeclensionInput = $("#word-declension-input");
const wordCojugationInput = $("#word-conjugation-input");
const setCheckBoxes = $(".set-checkbox");

// ------------------------------------------------------------------------- Global Variables

let editWordID; // Word that is currently beind edited in the admin from
let editAction = "NONE"; // State variable to control whether a word is being added or updated

// ------------------------------------------------------------------------- Event Listeners

closeAdminEditModalButton.on("click", () => {
  closeAdminEditModal();
});

adminEditFormSaveButton.on("click", () => {
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

// ------------------------------------------------------------------------- Functions

function showAdminEditModal(wordId) {
  // Populate the fields with word data if is editinng words
  if (editAction === "UPDATE") {
    // Find the relevant objecty from the wordData array
    editWordID = wordId;
    const wordObject = wordData.find((obj) => obj["word_id"] == wordId);

    populateAdminEditFields(wordObject);
    populateSetCheckBoxes(wordId);
  } else if (editAction === "ADD") {
    clearAdminEditFields();
    clearSetCheckBoxes();
  }

  adminEditModal.removeClass("hidden");
  backgroundOverlay.removeClass("hidden");

  backgroundOverlay.off("click");

  backgroundOverlay.on("click", () => {
    adminEditModal.addClass("hidden");
    backgroundOverlay.addClass("hidden");
  });
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
  wordPartOfSpeechInput.val(wordObject["word_part_of_speech"]);
  wordPronounceInput.val(wordObject["word_pronounciation"]);
  wordPronounceAudioInput.val(wordObject["word_pronounciation_audio"]);
  wordDefinitionInput.val(wordObject["word_definition"]);
  wordExplainInput.val(wordObject["word_explanation"]);
  wordExamplesInput.val(JSON.stringify(wordObject["word_examples"], null, 2));
  wordDeclensionInput.val(
    JSON.stringify(wordObject["word_declension"], null, 2)
  );
  wordAspectInput.val(
    JSON.stringify(wordObject["word_aspect_examples"], null, 2)
  );
  wordCojugationInput.val(
    JSON.stringify(wordObject["word_conjugation"], null, 2)
  );
}

function clearAdminEditFields() {
  // Generate a random eight-digit number
  randomId = Math.floor(10000000 + Math.random() * 90000000);
  wordIdInput.val(randomId);
  wordUkrInput.val("");
  wordEngInput.val("");
  wordRomanInput.val("");
  wordGenderInput.val("");
  wordPronounceInput.val("");
  wordPronounceAudioInput.val("");
  wordExplainInput.val("");
  wordExamplesInput.val("");
  wordDeclensionInput.val(JSON.stringify({ value: null }, null, 2));
  wordAspectInput.val(JSON.stringify({ value: null }, null, 2));
  wordCojugationInput.val(JSON.stringify({ value: null }, null, 2));
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

function clearSetCheckBoxes() {
  setCheckBoxes.each(function () {
    $(this).prop("checked", false);
  });
}

function submitWordEditUpdate() {
  // Get the form data object
  const formData = new FormData(
    document.getElementById("admin-word-edit-form")
  );

  // Parse the word JSON fields to JSON
  wordExamples = {};
  wordAspect = {};
  wordDeclension = {};
  wordConjugation = {};
  try {
    wordExamples = JSON.parse(formData.get("word_examples"));
    wordAspect = JSON.parse(formData.get("word_aspect_examples"));
    wordDeclension = JSON.parse(formData.get("word_declension"));
    wordConjugation = JSON.parse(formData.get("word_conjugation"));
  } catch (error) {
    showAlertModal("ERROR", `Error in usage examples syntax`);
    console.log(`Error in usage examples syntax (${error})`);
    return;
  }

  // Convert the form data to JSON
  const jsonData = {
    word_id: Number(formData.get("word_id")),
    word_ukrainian: formData.get("word_ukrainian"),
    word_english: formData.get("word_english"),
    word_roman: formData.get("word_roman"),
    word_gender: Number(formData.get("word_gender")),
    word_part_of_speech: Number(formData.get("word_part_of_speech")),
    word_pronounciation: formData.get("word_pronounciation"),
    word_pronounciation_audio: formData.get("word_pronounciation_audio"),
    word_definition: formData.get("word_definition"),
    word_explanation: formData.get("word_explanation"),
    word_examples: wordExamples,
    word_aspect_examples: wordAspect,
    word_declension: wordDeclension,
    word_conjugation: wordConjugation,
  };
  // ------------------------------------------------------ Update Word Logic
  if (editAction === "UPDATE") {
    showAlertModal("INFO", "Updating word...");
    fetch(`/api/words/update/${editWordID}`, {
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
    // ------------------------------------------------------ ADD Word Logic
    showAlertModal("INFO", "Adding word...");
    // Logic to run if adding a word record
    fetch(`/api/words/add`, {
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
        showAlertModal(data.status, data.message);
        // If the operation was successful update the current edit word id to the newly created word
        if (data.status === "SUCCESS") {
          editWordID = jsonData["word_id"];
        }
      });
  } else if (editAction === "DELETE") {
    showAlertModal("INFO", "Deleting word...");
    // Logic to running if deleting a word record
    fetch(`/api/words/delete/${editWordID}`, {
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
        showAlertModal(data.status, data.message);
      });
  }
}

function addDeleteSet(setId, addSet) {
  if (addSet) {
    showAlertModal("INFO", "Adding to set...");
    fetch(`/api/words/sets/${setId}/add/${editWordID}`, {
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
        showAlertModal(data.status, data.message);
      });
  } else {
    showAlertModal("INFO", "Removing from set...");
    fetch(`/api/words/sets/${setId}/delete/${editWordID}`, {
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
        showAlertModal(data.status, data.message);
      });
  }
}

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
