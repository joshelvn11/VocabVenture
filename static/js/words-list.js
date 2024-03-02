// Get the words list table
const wordsListTable = $("#words-list-table");

let wordData;

// Fetch the word data from the api
fetch("http://127.0.0.1:8000/api/words/list")
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
    // Iterate over the data and add a row for every element in the data
    console.log(wordData);
    for (let word of wordData) {
      console.log(word);
      wordsListTable.append(
        `<tr> 
        <td>${word["word_ukrainian"]}</td> 
        <td>${word["word_english"]}</td> 
        <td>${word["word_roman"]}</td> 
        <td>${word["word_pronounciation"]}</td>
        <td></td>
        </tr>`
      );
    }
  });
