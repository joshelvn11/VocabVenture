// Get the words list table
const wordsListTable = $("#words-list-table");

// Global word data variable, holds an array of word objects
let wordData;

// Get HTML elements
const wordDetailsModal = $("#word-details-modal");
const backgroundOverlay = $(".background-overlay");
const closeModalButton = $("#close-modal-button");
const detailsCardContainer = $("#details-card-container");
const wordUkr = $("#word-ukr");
const wordEng = $("#word-eng");
const wordPronounce = $("#word-pronounce");
const wordRoman = $("#word-roman");
const wordExplain = $("#word-explain");

// Add event listeners
closeModalButton.on("click", () => {
  closeModal();
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
  })
  .then((data) => {
    createTable();
  });

// Function to populate the table with the retrieved word data
function createTable() {
  // Iterate over the data and add a row for every element in the data
  for (let word of wordData) {
    // Create a formatted string from the English words array
    let englishWords = "";
    englishWords = formatArray(word["word_english"]);

    // Create the action button
    const showDetailsButton = $(`<button class="table-action-button">
              <svg
              width="64"
              height="64"
              viewBox="0 0 64 64"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              class="table-action-icon"
            >
              <path
                d="M2.7398 37.7833L10.4687 44.8101C16.3474 50.193 24.0292 53.1786 32 53.1786C39.9709 53.1786 47.6526 50.193 53.5313 44.8101L61.2591 37.7845C62.1224 36.9999 62.8121 36.0435 63.2842 34.9767C63.7562 33.9099 64 32.7562 64 31.5896C64 30.423 63.7562 29.2693 63.2842 28.2025C62.8121 27.1357 62.1224 26.1793 61.2591 25.3947L53.5313 18.3691C47.6528 12.9859 39.971 10 32 10C24.0291 10 16.3473 12.9859 10.4687 18.3691L2.7398 25.3959C1.87684 26.1804 1.18734 27.1367 0.715532 28.2033C0.24372 29.2699 0 30.4233 0 31.5896C0 32.7559 0.24372 33.9093 0.715532 34.9759C1.18734 36.0425 1.87684 36.9988 2.7398 37.7833ZM6.05307 29.0385L13.782 22.0117C18.756 17.4571 25.2557 14.9308 32 14.9308C38.7443 14.9308 45.244 17.4571 50.2181 22.0117L57.9458 29.0385C58.3017 29.3613 58.5861 29.7562 58.7807 30.1954C58.9753 30.6346 59.0759 31.1098 59.0759 31.5902C59.0759 32.0706 58.9753 32.5457 58.7807 32.985C58.5861 33.4242 58.3017 33.8179 57.9458 34.1406L50.2181 41.1675C45.2442 45.7225 38.7445 48.249 32 48.249C25.2556 48.249 18.7558 45.7225 13.782 41.1675L6.05307 34.1406C5.69752 33.8176 5.41343 33.4237 5.21903 32.9844C5.02463 32.5451 4.92421 32.07 4.92421 31.5896C4.92421 31.1092 5.02463 30.6341 5.21903 30.1948C5.41343 29.7554 5.69752 29.3616 6.05307 29.0385Z"
                fill="black"
              />
              <path
                d="M32 46.3623C34.9218 46.3623 37.7779 45.4959 40.2072 43.8727C42.6366 42.2494 44.53 39.9423 45.6481 37.2429C46.7662 34.5436 47.0588 31.5733 46.4888 28.7077C45.9187 25.8421 44.5118 23.2099 42.4458 21.1439C40.3798 19.0779 37.7476 17.671 34.882 17.101C32.0164 16.531 29.0461 16.8235 26.3468 17.9416C23.6475 19.0597 21.3403 20.9532 19.7171 23.3825C18.0939 25.8119 17.2275 28.668 17.2275 31.5897C17.2317 35.5063 18.7895 39.2613 21.559 42.0308C24.3284 44.8002 28.0834 46.358 32 46.3623ZM36.9242 24.2034C37.4112 24.2034 37.8872 24.3478 38.2921 24.6184C38.697 24.8889 39.0126 25.2734 39.1989 25.7233C39.3853 26.1732 39.434 26.6683 39.339 27.1459C39.244 27.6235 39.0095 28.0622 38.6652 28.4065C38.3209 28.7508 37.8822 28.9853 37.4046 29.0803C36.927 29.1753 36.4319 29.1266 35.982 28.9402C35.5321 28.7539 35.1476 28.4383 34.8771 28.0334C34.6065 27.6285 34.4621 27.1525 34.4621 26.6655C34.4628 26.0127 34.7224 25.3869 35.184 24.9253C35.6456 24.4637 36.2714 24.2041 36.9242 24.2034ZM31.4097 21.8008C30.1573 23.2011 29.4885 25.0278 29.5408 26.9058C29.5931 28.7838 30.3625 30.5704 31.6909 31.8989C33.0193 33.2273 34.806 33.9967 36.6839 34.0489C38.5619 34.1012 40.3886 33.4325 41.7889 32.18C41.6792 34.072 41.0248 35.8918 39.9045 37.4204C38.7842 38.9489 37.2458 40.1209 35.4747 40.7952C33.7035 41.4694 31.7752 41.6172 29.922 41.2206C28.0689 40.824 26.3699 39.9 25.0298 38.5599C23.6898 37.2199 22.7658 35.5209 22.3692 33.6677C21.9726 31.8145 22.1203 29.8862 22.7946 28.1151C23.4688 26.3439 24.6408 24.8056 26.1694 23.6852C27.6979 22.5649 29.5178 21.9105 31.4097 21.8008Z"
                fill="black"
              />
            </svg>
            </button>`);

    // Add the word's ID as a data attribute
    showDetailsButton.attr("word-id", word["word_id"]);

    // Add event listener to the show details button
    showDetailsButton.on("click", () => {
      showModal(showDetailsButton.attr("word-id"));
    });

    // Create the table row for the current word
    const wordRow = $(`<tr> 
        <td>${word["word_ukrainian"]}</td> 
        <td>${englishWords}</td> 
        <td>${word["word_roman"]}</td> 
        <td>${word["word_pronounciation"]}</td>
        </tr>`);

    // Create a <td> element to hold the action buttons
    actionButtonsElement = $("<td></td>");

    // Add the action buttons to the td element
    actionButtonsElement.append(showDetailsButton);

    // Append the action buttons element to the table row
    wordRow.append(actionButtonsElement);

    // Append the row to the table
    wordsListTable.append(wordRow);
  }
}

function showModal(wordId) {
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

function loadUsageExamples(wordObject) {
  console.log(wordObject["word_examples"]);
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
                            ${usageExample["english"][index]}
                        </div>`);
      tooltipContainer.append(englishTooltip);
      let romanTooltip = $(`<div class="interactive-word-tooltip">
                            ${usageExample["roman"][index]}
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

function closeModal() {
  // Hide the modal and background overlay
  wordDetailsModal.addClass("hidden");
  backgroundOverlay.addClass("hidden");

  // Remove all the usage example elements
  $(".usage-example").remove();
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
