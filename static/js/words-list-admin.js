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

let editWordID; // Word that is currently being edited in the admin form
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
  let confirmDelete = confirm(
    "Are you sure you want to delete this word? This action cannot be undone."
  );
  if (confirmDelete) {
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
  // Populate the fields with word data if editing words
  if (editAction === "UPDATE") {
    // Find the relevant object from the wordData array
    editWordID = wordId;
    const wordObject = wordData.find((obj) => obj["word_id"] == wordId);

    if (!wordObject) {
      showAlertModal("ERROR", "Word data not found.");
      return;
    }

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
  wordPartOfSpeechInput.val("");
  wordExplainInput.val("");
  wordDefinitionInput.val("");
  wordExamplesInput.val("");
  wordDeclensionInput.val(JSON.stringify({ value: null }, null, 2));
  wordAspectInput.val(JSON.stringify({ value: null }, null, 2));
  wordCojugationInput.val(JSON.stringify({ value: null }, null, 2));
}

function populateSetCheckBoxes(wordId) {
  fetch(`/api/words/sets/${wordId}`, {
    method: "GET",
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch set data.");
      }
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
    })
    .catch((error) => {
      showAlertModal("ERROR", `Failed to load set data: ${error.message}`);
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

  // Validate required fields
  const requiredFields = [
    "word_ukrainian",
    "word_english",
    "word_roman",
    "word_gender",
    "word_part_of_speech",
    "word_pronounciation",
    "word_pronounciation_audio",
    "word_definition",
    "word_explanation",
  ];

  const missingFields = requiredFields.filter((field) => !formData.get(field));

  if (missingFields.length > 0) {
    showAlertModal(
      "ERROR",
      `The following fields are required: ${missingFields.join(", ")}`
    );
    return;
  }

  // Validate that part of speech and gender are integers
  const wordPartOfSpeech = formData.get("word_part_of_speech");
  const wordGender = formData.get("word_gender");

  if (
    !Number.isInteger(Number(wordPartOfSpeech)) ||
    !Number.isInteger(Number(wordGender))
  ) {
    showAlertModal(
      "ERROR",
      "The fields 'Part of Speech' and 'Gender' must be integers."
    );
    return;
  }

  // Check if the audio is a vali url
  // code from https://medium.com/@tariibaba/javascript-check-if-string-is-url-ddf98d50060a
  try {
    const url = new URL(formData.get("word_pronounciation_audio"));
  } catch (error) {
    showAlertModal("ERROR", "Pronounciation audio must be a valid URL");
    return;
  }

  // Parse the word JSON fields to JSON
  let wordExamples = {};
  let wordAspect = {};
  let wordDeclension = {};
  let wordConjugation = {};
  try {
    wordExamples = JSON.parse(formData.get("word_examples"));
    wordAspect = JSON.parse(formData.get("word_aspect_examples"));
    wordDeclension = JSON.parse(formData.get("word_declension"));
    wordConjugation = JSON.parse(formData.get("word_conjugation"));
  } catch (error) {
    showAlertModal("ERROR", `Error in JSON syntax: ${error.message}`);
    console.log(`Error in JSON syntax (${error})`);
    return;
  }

  console.log(wordExamples);

  requiredKeys = ["ukrainian", "english", "roman", "index", "translation"];

  // Check if wordExamples is an array
  if (!Array.isArray(wordExamples)) {
    showAlertModal("ERROR", `Usage examples needs to be an array of objects`);
    return;
  }

  // Check each word example cotains the required keys
  for (let i = 0; i < wordExamples.length; i++) {
    if (!requiredKeys.every((key) => key in wordExamples[i])) {
      showAlertModal(
        "ERROR",
        `The usage example at index ${i} is missing one of the required keys`
      );
      return;
    }
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
        if (!response.ok) {
          throw new Error("Failed to update word.");
        }
        return response.json();
      })
      .then((data) => {
        showAlertModal(data.status, data.message);
      })
      .catch((error) => {
        showAlertModal("ERROR", `Update failed: ${error.message}`);
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
        if (!response.ok) {
          throw new Error("Failed to add word.");
        }
        return response.json();
      })
      .then((data) => {
        showAlertModal(data.status, data.message);
        // If the operation was successful update the current edit word id to the newly created word
        if (data.status === "SUCCESS") {
          editWordID = jsonData["word_id"];
        }
      })
      .catch((error) => {
        showAlertModal("ERROR", `Add failed: ${error.message}`);
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
        if (!response.ok) {
          throw new Error("Failed to delete word.");
        }
        return response.json();
      })
      .then((data) => {
        showAlertModal(data.status, data.message);
      })
      .catch((error) => {
        showAlertModal("ERROR", `Delete failed: ${error.message}`);
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
        if (!response.ok) {
          throw new Error("Failed to add to set.");
        }
        return response.json();
      })
      .then((data) => {
        showAlertModal(data.status, data.message);
      })
      .catch((error) => {
        showAlertModal("ERROR", `Add to set failed: ${error.message}`);
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
// code from https://www.reddit.com/r/django/comments/17jbsj3/react_post_django_view_problems/
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
