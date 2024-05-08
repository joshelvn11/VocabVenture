# VocabVenture

![Device Mockups](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/device-mockup.png)

VocabVenture is a language learning web app that currently supports learning Ukrainian from English. The app is designed to be easy, simple, and straightforward to use, focusing on learning through repetition and practical examples. I created the app in response to my dissatisfaction with many "over-gamified" solutions (such as Duolingo), where I felt that my brain and memory were not being adequately challenged to create new neural pathways. This lack of challenge hindered the effective cementing of new words into my vocabulary, impeding substantial progress in language learning.

VocabVenture adopts the traditional but effective approach of learning through constant testing and repetition. It is aimed at individuals who prefer this method of learning. The app features an extensive word list with crucial information needed to understand each word, its meaning, appropriate usage, and semantic and grammatical nuances. While the information on each word is comprehensive, most of it is optional. This design choice ensures that while additional details can enhance understanding, they are not necessary for gaining a basic and practical understanding of the word. The app is designed to initially hide detailed information to prevent overwhelming users, but it remains easily accessible for those who wish to engage more deeply.

So to summarise this information into one succinct goal, the goal would be to effectively teach newcomers to the Ukrainian language basic vocubulary and beyond so can start to properly learn the language by studying further through reading, writing, listening and speaking. It is designed to give a firm foundation in vocabulary for further exploration to allow further linguistic exploration.

## Backend

The backend of the application is built with Django. Pages are primarily server-side rendered, with some client-side updates performed using the application's REST API, built with Django's Rest Framework. Updates to database data are made by the client via the REST API. Certain incremental jobs are carried out by a cron job on a separate server that requests specific endpoints to execute job functions (e.g., resetting streaks at midnight every night).

## The Layout & Structure

### Home

The home screen serves as the primary entry point into the application, displaying overall stats and statistics for the current user, including streaks, overall progress, and the learning stages of all words that the user has started learning.

### Alphabet

This page simply displays the Cyrillic alphabet with approximated English pronunciations for constant reference during learning.

### Words

The Words page is the central focal point of the application, displaying a list of categorized sets of words. For each set, the current logged-in user's scores are shown. Clicking on any set displays a list of all the words contained within that set as cards, with the word in the target language as the card title and some basic essential information about that word underneath, including the translation, romanization, and pronunciation.

Clicking on any word brings up a modal displaying more detailed information about the target word, including a definition, explanation, and practical usage example that are interactive. Hovering (or clicking on mobile) over any word in the usage example shows the contextual translation and romanization in tooltips, and underneath, a 'show translation' button can be clicked to show the translation of the entire sentence. This feature allows learners to understand the direct translation of words in their context while preserving the overall meaning of the communication. The usage examples are dynamically generated from JSON data stored in the database, making it easy for an admin to create new interactive examples simply by following the JSON data format.

## Features & Functions

### Intro Tour Messages

To enhance UX and usability, every page and feature has a message displayed explaining what it is and how to use it. Once the message has been closed by the user, it will not be displayed again, as the state of the message for that specific user is persisted to the database.

### Home Screen & Stats

The main entry point of the app is the home screen, where users can see various stats related to their account, including:

1. Quiz Current Streak - how many consecutive days they have taken a test quiz for each respective quiz type.
2. Quiz Longest Streak - their longest recorded streak for each respective quiz type.
3. Word Progress - their overall word progress for all the words in the app. This shows the progress of how many words they have a score for out of all the overall words in the app, broken down and color-coded by the number of words in each learning stage (New, Learning, Learned, Mastered).
4. Learning Stage Breakdown - these are separate cards showing the percentage of words the user has scores for in each learning stage.

![Home Screen Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/home-screen.png)

### Alphabet

This is a full list of letters in the Cyrillic alphabet, showing approximate pronunciations for each letter.

![Alphabet Screen Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/alphabet.png)

### Word Sets

In the app, all words are divided into sets for easier and more structured learning; words can be in multiple sets. The sets page displays these sets and allows users to navigate to the page containing all words in that set by clicking on the set item. The sets also show stats for the user scores in each specific set. It shows the average score of all the words, broken down by quiz type and the overall word score.

![Word Sets Screen Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/word-sets.png)

### Word Lists

The word list page displays a list of the words in the respective set that was accessed. Each word is displayed as a card with the word in Ukrainian as the main card element and the most basic and essential info about the word, including the English translation, romanization, and pronunciation. It also displays a progress bar showing the overall word score progress for the word, which is an average of the three quiz scoring metrics. By clicking on a word, a modal is displayed showing further details about the word.

When the word list is accessed, this page is always dynamically generated; however, the extended word details are also loaded in behind the scenes via an API call to the server on page load. This reduces database requests and speeds up performance when the word details modal is shown.

![Word List Screen Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/word-list.png)

### Word Details

The word details modal can be accessed by clicking on any word in the word list screen. Clicking on a word will open this modal, which shows further information about the word being accessed. The data in the modal is dynamically generated from the data loaded from the API in the previous step. The word details modal also contains the relevant score data for the various quiz types of the current word being viewed. Clicking the audio button at the top allows the user to hear the pronunciation of the current word.

![Word Details Screen Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/word-details.png)

### Usage Examples

The usage examples are an interactive element of the word details modal where users can see the word in the context of an actual Ukrainian sentence. Hovering over any word in the sentence allows the user to see the romanization of that word and the direct translation of the word in the context of the current sentence. Clicking the 'Show Translation' button underneath the sentence will show the overall translation of that sentence.

The interactive usage examples are dynamically generated from data stored as JSON when the modal is opened. Storing the data as JSON and creating an automatic rendering process for the interactions makes it very simple for non-technical admins to create these interactive elements.

![Usage Examples Screen Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/usage-examples.png)

### Quiz

The quiz component of the app is probably the most integral part next to the words themselves, as it is the part that allows users to practice and really improve their vocabulary.

There are currently two quiz types players can use to practice: a flashcard quiz and a spelling quiz, each of which are described in further detail below.

Furthermore, each quiz type can be played in two different modes: Practice and test mode. In practice mode, questions are repeated until the user gets them right, and answers are not scored, meaning a correct answer does not contribute any points to a word's score, and a wrong answer does not deduct any points from a word's score.

Currently, only the predefined word sets can be quizzed, and this can be accessed by clicking the 'Quiz' button at the top of any set. Upon clicking the button, the user is presented with a modal allowing them to select the quiz type they wish to use and whether or not to quiz in practice or test mode. When the 'Start Quiz' button is clicked, the quiz is then started with the configuration they chose.

![Quiz Modal Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/quiz-modal.png)

#### Flashcard Quiz

The flashcard quiz type is probably a familiar concept to everyone. When the user opts to take a flashcard quiz, two cards are generated for every word in the set, one for Ukrainian to English and one for the reverse, English to Ukrainian. These cards are then shuffled and generated into interactable card elements for the user to play with.

How it works is a card is shown with the question side facing the user, the question asking for the translation of the Ukrainian or English word depending on which card is being shown. The user can then flip the card and select whether they were correct or incorrect.

In practice mode, if they are correct, the card is removed from the deck, and they proceed to the next card. If they are incorrect, the card is moved to the end of the deck, where they can attempt it again. This continues until all cards are correctly guessed.

In test mode, the same process happens with a correct answer, and their score for that word is incremented. If they get an answer incorrect in test mode, the word is also removed from the deck but this time not added onto the end, and their score for that word is decremented.

Once they have finished the quiz, they can choose to restart or exit the quiz.

![Flashcard Quiz Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/flash-cards.png)

#### Spelling Quiz

The spelling quiz allows users to test and practice their memory and spelling while also learning the meaning of words in the context of a sentence at the same time.

When the user accesses the spelling quiz, a set of 'spelling cards' are generated for the current set, shuffled, and displayed to the user. On each card is an instruction giving the English translation that needs to be filled in, an interactive sentence like in the usage examples, but where the focus word is, there is an input field for the user to fill in the missing word. It also includes a 'Show Translation' button to show the overall translation of the sentence.

In practice mode, the answer is shown as a hint for the input, so the user can see the answer until they enter any character, at which point the hint will disappear. Showing the answer like this and letting the user type it in may seem counter-productive but is essential for building that muscle memory for learning words. In a similar fashion to the flashcards, if the user gets the answer incorrect in practice mode, the card will be repeated, except this time not at the end. The card is immediately shown again until the user gets the correct answer.

In test mode, the key difference is that no word hint is shown, so the user needs to remember it completely from their own memory. The rest of the test mode functionality is the same as the flashcard test mode, being that questions are not repeated when incorrect, and users' scores are incremented/decremented if they get a question correct/incorrect.

![Spelling Quiz Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/spelling-quiz.png)

### Scoring

The scoring system is fairly simple; every word has three scoring metrics:

1. Flashcard Score - the score contributed to by answering Flashcards that are Ukrainian to English
2. Flashcard Score (Reverse) - the score contributed to by answering Flashcards that are English to Ukrainian
3. Spelling - the score that is contributed to by answering spelling questions

Each word then has a total score, which is the average of these scores.

Every set also has the scores calculated for each user. It has each of the same three score metrics, which is calculated by taking the score for each score metric for each word in the set, then calculating an average of all the words in the set. The set total is then calculated by taking the sets three scores and finding the average.

In tests, every correct answer increments the word score by 20 points, and every incorrect answer decrements the score by 5 points.

Every word is divided into four different learning stages based on the word's score:

1. New - 0 to 24%
2. Learning - 25% to 74%
3. Learned - 75% to 99%
4. Mastered - 100%

### Admin Editing

Admins are able to add, delete, and edit word data on the front end of the app using API calls to the server. Using custom-built forms on the front end and submitting data via API calls prevents the need for page reloads, ultimately resulting in a better user experience.

To access word addition functionality, the admin can navigate to any set where they will see the button to add a word; this button is only available if the user is authenticated as a superuser. Clicking this brings up a modal with a form with all required fields for the data necessary to create a new word object. There is also a checklist of sets that is dynamically generated by getting all the existing sets from the server via an API call. Once the word is created, the admin can then check (or uncheck) sets they want the word to be in. Some of the fields are prepopulated with data, such as the Word ID, which is a random eight-digit number.

Each field is first validated on the client side and then again validated by the model's serializer on the server side. Any error in any of these validations will alert the user to the error by an alert pop-up.

The user is also alerted to every successful action, such as adding a word or adding the word to a set.

![Word Add Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/word-add.png)

If the admin wishes to edit the word, they can navigate to the word details modal and click the edit button, which will bring up the same modal but prepopulated with all the data of the current word being edited.

![Word Edit Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/word-edit.png)

### Navigation Bar

The navigation bar is designed to be simple and easy to use; it is located on the left of the screen and is always visible to the user on desktop. On mobile, it collapses, and a hamburger menu button becomes available to expand the menu. The menu can then be closed by hitting the close button or clicking anywhere off the menu.

The menu links are outlined and colored using the primary color of the application to indicate to the user which page they are currently on.

### Profile

The profile system is currently very basic and just allows the user to see they are logged in with the correct profile and log out if they need to. The profile button is located at the bottom of the navigation bar to separate it from all the app functions and so it is always accessible to the user. Clicking the profile button expands a small menu where they can see their username and email and includes a log-out button to log out of the app.

### Alert Notifications

I created a custom alert notification system to show alerts to the user to update them on any important information and give them feedback about their actions or if there are any errors.

There is a fixed container located in the upper right-hand corner used to hold and display alert notifications. It operates as a stack, so multiple alert notifications can be stacked on top of one another if multiple alerts occur in a short space of time.

The alert notifications are split into four categories: Info, Warning, Error, and Success. Each alert is color-coded, and the alert will be outlined in the alert color as well as the alert title set to the name of the alert category. This makes it easy for users to understand the purpose and intent of the message.

Messages can be closed manually using the close icon on each alert but will also close automatically after eight seconds.

![Alert Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/alerts.png)

### Login / Sign Up

The login and sign-up system uses all of Django's default authentication system functionality; however, I have customized the styling heavily to be as user-friendly as possible and in line with the design of the rest of the application, as well as also being in line with the conventional login/sign-up form look that users will probably be used to.

There is also a link to each alternate page at the bottom of the form to allow users to easily navigate between each page.

![Login Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/login.png)

![Sign Up Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/sign-up.png)

### Progressive Web App

VocabVenture is also a progressive web app, which improves performance and allows users to install it like a native app on mobile devices for a greatly enhanced user experience. I achieved this using the Django PWA module, which made it very simple to implement.

## API

For this application, I created a custom REST API using Django's Rest Framework. I adopted this approach for multiple reasons, firstly being that while most of the site is rendered on the server, I want some components to be only rendered when necessary and prevent unnecessary database calls and rendering on the server for components that may not even be used. It also allowed the client to make updates to data without having to reload pages, such as when updating scores or word data. These use cases all use Django's authentication tokens to verify the access level of the user accessing the API. Some API endpoints are public, meaning users do not have to be logged in to access them, which is useful if other applications wish to use the application's data.

The other purpose is for running scheduled jobs on the database, such as updating user streaks at midnight every night. I had initially attempted to use celery and rabbitmq as a message broker to achieve this but ran into some limitations using the approach with the hosting I was using, so I instead opted to make job functions accessible as an API endpoint that is then called at set intervals by a cron job on another server, specifically I have used cron-job.org to accomplish this. These job requests are authenticated using a secret access token as a parameter when making requests.

## Database

### Schema

![VocabVenture Database ERM](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/vocab-venture-erm.png)

[View the ERM on Figma here](https://www.figma.com/file/Zhc99JR3FgcUm0Vguyzy6w/Vocab-Venture-ERM?type=whiteboard&node-id=0%3A1&t=aZP744msjxiJwk40-1)

## Design

The design of the app is focused on overall simplicity and usability for the best overall user experience. It adopts a mainly card-based design to easily segment information into manageable and identifiable chunks to make the information easier to consume and generally less overwhelming. It follows a fairly conventional design approach adopted by many other popular apps and websites to ensure it is easy and intuitive to use for all levels of users.

The app design, in general, was developed from a mobile-first approach to ensure mobile users were considered as the primary users and to make the mobile experience as best as possible.

The colors are kept simple as well, using black and white for most of the app and highlighting specific important elements using the primary color where needed. Buttons also show their level of importance by using either a solid background or white background with a border to denote the significance and priority of the button.

You will also notice subtle yet valuable animations all over the app to give immediate feedback to the user about the state and result of their interactions with the app.

The app was designed in Figma before being developed.

### UI Design Mockup

[View the Mockup on Figma here](https://www.figma.com/file/P8PLJER8rZtrxbMYkEH8Wz/Vocab-Venture-Design?type=design&mode=design&t=cU2YagP9xr99O5fx-1)

## Deployment

### Web App

The application itself is currently deployed to a Render Web Server instance and the database to a Render database instance.

The deployment process follows these steps:

1. Create a Render web service instance.
2. Select 'Deploy from Github repo'.
3. Connect the relevant repo.
4. Add necessary environment variables for the database URL, disable collectstatic value, and the job secret key (used for running remote cron jobs).
5. Finalize the creation.
6. The web service will now deploy from the Github repo and on every subsequent push to the repo.

### Database

The database is a PostgreSQL database also running using Render, which automates the process of database deployment and management.

### Object Storage

The app uses Wasabi's S3 compatible storage platform for all object-based storage.

## Future Ideas / Roadmap

### AI Chat

Implement an AI-based chat feature where all messages can be broken down and analyzed like has been done with the usage examples

### Phrase Library

Similar to the word library, I would like to include a library of full phrases that users can get info and quizzed on in a similar way to words.

### Multiple Languages

This entails rewriting some of the application logic to dynamically generate UI components based on the target language's data model based on what data needs to be included about the target language. For example, languages that use the Roman alphabet would not need an alphabet section or to show the romanized form of words.

## Testing

### Validator Testing

#### W3C HTML Validator

The HTML unfortunately did pass through the validator with a few errors; however, most were necessary for the application to work and are not critical nor inhibit function in any way. For example, I have an error that the letter-id or word-id attribute is not allowed on a div element, but this was my method for retrieving data from the DOM element to know what word to display details for on the word details modal when it is shown.

There were also a couple of errors related to certain sizes not being set on link elements to do with PWA icons; however, these are auto-generated by Django, and I couldn't seem to find a way to edit them directly.

#### Jigsaw CSS Validator

The CSS passed through the validator with no errors.

#### PEP8 Validator

All custom Python code was checked against PEP8 style guidlines using the pep8 and pycodestyle command lines tools. It mostly passes
without issues with exception to multiple occurrences of warning regarding lines being to long, which were left like they are
intentionally. Where possible I followed convention to line length however where I felt shortening the line length as per guidance
created a negative readability experience and since the whole point of PEP8 is to prove readability and maintainability it seemed
counterintuive to blindly follow the guidlines even it worked against the direct goal it is meant to have. Often where these lines
that are too long occur are with "non-functional" code for example strings for long urls or json sample data.

### Python Testing

All Django views are tested extensively using Django's in-built unit testing framework. Multiple test cases are carried out for every view function testing for factors such as authorization, correct responses, data validity, and correct template rendering.

During unit tests, a separate PostgreSQL test database is created on Neon and used for testing purposes, where it is then destroyed at the end of every test run.

### JavaScript Testing

All JavaScript was tested extensively in a few ways. Firstly, as JS is primarily used to control UI interactions on the page, it was tested manually by going through all possible interactions and testing that the JS manipulated or created the UI in the intended way following the test cases outlined below.

Where JS was used to manipulate data via API calls, all data being sent and responses being received were printed to the console and analyzed to ensure data validity and integrity. All errors are also caught and displayed to the console to catch and fix these errors. Many of the API calls made by the JS don't originate from user-entered data to reduce the chance for any invalid data being passed, for example, score data where the data generated is generated by the JS on the binary factor of if the user got an answer right or wrong. The data sent using JS was also checked when incoming on the server end by getting Django to print out API requests to the console and checking what had been passed.

Currently, only manual unit testing was carried out as I am still having issues with getting the test environment to work correctly based on the tech stack and jQuery; as soon as that is resolved, automated unit tests will be added.

It is critical when running these JavaScript manual tests that the automated Python/Django tests are run first to ensure they are not the cause of any issues. Many of the JavaScript processes and functions are dependent on receiving the correct input from Django. If all Django unit tests pass without issue, then it can be logically assumed that any failures in the tests below must result from the JavaScript.

#### Test Case 1: Alert notifications are shown

- **Objective**: Verify that the notification alert is able to be displayed correctly
- **Steps**:
  - Ensure the test alert button is using the correct parameters needed by the showAlertModal() function (type, message)
  - Click the test flashcard button invoking the showAlertModal() function
  - Observe the result in the UI.
- **Expected Results**:
  - The alert notification pop-up is shown showing the relevant message type as the heading and the message passed as the alert body.
  - When called multiple times in a row, the alerts stack on top of each other
  - Each alert modal is automatically closed after eight seconds.
  - If the alert modal close button is clicked, the relevant alert modal is closed.
- **Pass/Fail**: Pass if all the expected results occur; otherwise, fail.

#### Test Case 2: Word detail data fetch from API

- **Objective**: Verify that word detail data is being fetched correctly from the API on any word list page.
- **Steps**:
  - In the final promise of the fetch method used to fetch the word data from the API in word-list.js, add a console.log statement to log the JSON object fetched from the API to the console.
  - Navigate to any word list page of any set that is populated with the word data.
  - Open the developer console and refresh the page.
  - Wait a few seconds for the result of the API fetch to be printed to the console.
- **Expected Results**:
  - An array of JSON objects is printed to the console
  - The length of the array is equal to the number of words in the set being accessed.
  - The keys of each JSON object match the fields of the WORD model in the database
  - The values of each field in the JSON object match the values in the database for the words in the current set.
- **Pass/Fail**: Pass if all the expected results occur; otherwise, fail.

#### Test Case 3: Word details modal

- **Objective**: Verify that word details shown with the data that matched the word being accessed.
- **Steps**:
  - Click on any word in the word list of any set.
  - Observe the data in the word details modal that is shown.
- **Expected Results**:
  - When the card of any word is clicked, a modal pop-up is shown.
  - The contents of the modal match the data in the database for which word was accessed.
  - The scores for the current word being accessed match the scores as reflected in the database.
  - The number of usage examples shown match the number of usage examples created for the current word.
- **Pass/Fail**: Pass if all the expected results occur; otherwise, fail.

#### Test Case 4: Usage example interactivity

- **Objective**: Verify that the usage examples are rendered correctly and when interacted with display the correct data.
- **Steps**:
  - Click on any word in the word list of any set.
  - Observe the usage examples shown for that word.
  - Hover over every word and observe the results.
  - Click the 'Show Translation' button and observe the results
- **Expected Results**:
  - Each usage example shows the Ukrainian words of the current usage example correctly as one unbroken sentence.
  - When any word is hovered over, the correct corresponding romanization and English word are shown above the word.
  - When the 'Show Translation' button is clicked, the text of the button changes to the corresponding sentence translation for the current usage example
- **Pass/Fail**: Pass if all the expected results occur; otherwise, fail.

#### Test Case 4: Word audio for invalid audio

- **Objective**: Verify that the word audio button is displayed and works correctly for a word with valid audio data.
- **Steps**:
  - Verify that the word being tested contains a valid audio file link
  - Open the word details modal for the word being tested.
  - Click on the audio button and observe the results
- **Expected Results**:
  - When the word details modal is open, the 'Audio' button is shown.
  - When the 'Audio' button is clicked, the matching pronunciation audio is played.
- **Pass/Fail**: Pass if all the expected results occur; otherwise, fail.

#### Test Case 5: Word audio for invalid audio

- **Objective**: Verify that the word audio button is not displayed and an alert is shown for words with an invalid audio link.
- **Steps**:
  - Verify that the word being tested contains an invalid audio file link by giving an invalid extension or changing the file name to one that does not exist.
  - Open the word details modal for the word being tested.
  - Observe the results
- **Expected Results**:
  - When the word details modal is opened, the 'Audio' button is not shown.
  - An alert is shown saying that there was an error loading the pronunciation audio for the current word.
- **Pass/Fail**: Pass if all the expected results occur; otherwise, fail.

#### Test Case 6: Add word functionality with valid data

- **Objective**: Verify that the add word modal is displayed to admin and can successfully add a word with valid data
- **Steps**:
  - Log in as a superuser
  - Navigate to any word list page
  - Click the 'Add Word' button
  - Enter valid data into all fields
  - Click the 'Save' button
- **Expected Results**:
  - When the 'Add Word' button is clicked, a modal is displayed with fields corresponding to all fields for the WORD model in the database.
  - An eight-digit word id is automatically generated.
  - When the 'Save' button is clicked, an alert is shown saying the word was successfully added, and the new word appears in the database.
- **Pass/Fail**: Pass if all the expected results occur; otherwise, fail.

#### Test Case 7: Add word functionality with invalid data

- **Objective**: Verify that the word add modal cannot add a word to the database that has any invalid data, and this is notified to the user.
- **Steps**:
  - Log in as a superuser
  - Navigate to any word list page
  - Click the 'Add Word' button
  - Enter invalid data into all fields, such as blank fields or an invalid URL or JSON object into relevant fields
  - Click the 'Save' button
- **Expected Results**:
  - When the 'Save' button is clicked, an alert is shown saying the word could not be added to the database because of invalid data and a description of the invalidity.
  - The word that was attempted to be added does not appear in the database
- **Pass/Fail**: Pass if all the expected results occur; otherwise, fail.

#### Test Case 8: Edit word functionality with valid data

- **Objective**: Verify that the edit word modal correctly loads data and makes edits to the database
- **Steps**:
  - Log in as a superuser
  - Navigate to any word list page
  - Click any word on the word list page
  - Click on the 'Edit Word' button
  - Edit any fields with valid data
  - Click the 'Save' button
- **Expected Results**:
  - When the 'Edit Word' button is clicked, the word edit modal is displayed with the fields populated with the correct data for the corresponding word being edited.
  - The set checkboxes are automatically checked for the sets that correspond with the word being tested.
  - When the data is saved, an alert notification is shown stating that the data has been edited successfully.
  - The edits are reflected in the database.

#### Test Case 9: Edit word functionality with invalid data

- **Objective**: Verify that the edit word modal cannot make edits to any words in the database using invalid update data, and this is notified to the user.
- **Steps**:
  - Log in as a superuser
  - Navigate to any word list page
  - Click any word on the word list page
  - Click on the 'Edit Word' button
  - Edit any fields using invalid data
  - Click the 'Save' button
- **Expected Results**:
  - When the 'Save' button is clicked, an alert is shown saying the word could not be updated in the database because of invalid data and a description of the invalidity.
  - The updates that were attempted are not reflected in the database

#### Test Case 10: Delete word functionality

- **Objective**: Verify that the delete word functionality works correctly by deleting the chosen word from the database
- **Steps**:
  - Log in as a superuser
  - Navigate to any word list page
  - Click any word on the word list page
  - Click on the 'Delete' button
- **Expected Results**:
  - When the 'Delete' button is clicked, an alert is shown stating that the word was successfully deleted from the database
  - The word no longer appears in the database

#### Test Case 11: Quiz start modal

- **Objective**: Verify that quiz start modal is shown and works correctly
- **Steps**:
  - Log in into the application
  - Navigate to any words lists page of any set
  - Click the 'Quiz' button
  - Adjust the settings as desired (repeat test using different settings)
  - Click on the 'Start Quiz' button
- **Expected Results**:
  - When navigating the word list page of any set, the 'Quiz' button is shown.
  - Clicking on the 'Quiz' button will bring up the quiz modal.
  - Clicking on the 'Start Quiz' button will direct a user to the URL matching the current set and containing parameters matching the settings that were configured in the modal for quiz type and practice mode.

#### Test Case 12: Flashcard quiz general functionality

- **Objective**: Verify that common functionality for flashcard practice/test mode works correctly.
- **Steps**:
  - Adjust the settings in the quiz modal to be the Flashcard quiz type and start the quiz.
  - Click the 'Flip' button and observe results.
  - Click the 'Correct' button and observe results.
  - Click the 'Flip' button again.
  - Click the 'Incorrect' button and observe results.
  - Continue until the end card is reached.
  - Click the 'Restart' button.
  - Repeat the process again until the end card is reached and click the 'Return' button
- **Expected Results**:
  - When directed to the flashcard quiz page, the page is displayed correctly.
  - The initial cards remaining value is equal to double the number of words in the set (two cards for each word).
  - A card with valid data matching a random word in the set is shown.
  - The 'Correct' and 'Incorrect' buttons are inactive and cannot be clicked/used.
  - When the 'Flip' button is clicked, the card is flipped over, revealing the answer for the corresponding question.
  - Also, when the flip button is clicked, the 'Correct' and 'Incorrect' buttons become active and usable.
  - When the 'Correct' or 'Incorrect' buttons are clicked, the card flashes the corresponding color, changes to the next card, the cards remaining is decreased by one, and the buttons are set to be inactive again.
  - If the answer or question card is a Ukrainian word, the 'Show Romanisation', 'Show Pronunciation', and 'Play Audio' buttons are shown.
  - When the 'Restart' button is clicked, the cards remaining is set to the original quantity, and a valid flashcard is displayed.
  - When the 'Return' button is clicked, the user is redirected to the word list for the set they were previously on.

#### Test Case 13: Flashcard quiz practice functionality

- **Objective**: Verify that practice-specific functionality of the flashcard quiz works correctly
- **Steps**:
  - Check scores for all words in the set you are about to quiz.
  - Adjust the setting in the quiz modal to be for the flashcard quiz type and practice mode being on.
  - In the quiz, after clicking the 'Flip' button, click the 'Incorrect' button.
  - Continue and finish the quiz using either 'Correct' or 'Incorrect.
  - Once the quiz is finished, recheck all the scores for the words in the set that was tested.
- **Expected Results**:
  - When the 'Incorrect' button is clicked, the cards remaining does not decrease, and the flashcard is shown again after all other cards
  - After the quiz is finished, none of the scores should have been changed.

#### Test Case 14: Flashcard quiz test functionality

- **Objective**: Verify that test-specific functionality of the flashcard quiz works correctly
- **Steps**:
  - Check scores for all words in the set you are about to quiz.
  - Adjust the setting in the quiz modal to be for the flashcard quiz type and practice mode being off.
  - Play the quiz, choosing 'Correct' for every word
  - Once the quiz is finished, recheck all the scores for the words in the set that was tested.
  - Repeat the process using choosing 'Incorrect' for every word.
- **Expected Results**:
  - After the quiz is finished just using correct, all the word Flashcard scores should have been incremented by 20.
  - After the quiz is finished just using incorrect, all the word Flashcard scores should have been decremented by 5.

#### Test Case 15: Spelling quiz general functionality

- **Objective**: Verify that common functionality for spelling practice/test mode works correctly.
- **Steps**:
  - Adjust the setting in the quiz modal to be for the spelling quiz type
  - Click the 'Start Quiz' button
  - Hover over every word in the example sentence and observe results.
  - Click the 'Show Translation' button and observe results
  - Enter the correct answer for the current word and click 'Check'
  - Enter the incorrect answer for the current word and click 'Check'
- **Expected Results**:
  - After the 'Start' Quiz button is clicked, the user is directed to the spelling test screen.
  - The number of words remaining is equal to the number of words in the current set minus one.
  - When any word in the example sentence is hovered over, the romanization and translation of that word are shown.
  - When the 'Show Translation' button is clicked, the button text is changed to the correct corresponding translation of the current word.
  - When moving to the next card, the show translation button is reset, and all the question content is adjusted for the next word in the set.

#### Test Case 17: Spelling quiz practice functionality

- **Objective**: Verify that test-specific functionality for spelling quiz works correctly.
- **Steps**:
  - Adjust the setting in the quiz modal to be for the spelling quiz type and practice mode to be on.
  - Click the 'Start Quiz' button
  - Enter the incorrect spelling in the input field, click the check button and observe results.
  - Enter the correct spelling in the input field, click the check button and observe results.
  - Enter the correct spelling in the input field, click the check button and observer results.
  - Keep entering correct spellings until the set of flashcards is finished.
- **Expected Results:**
  - When the quiz in accessed is practice mode the correct answer is shown as a hint in the input field and disappears when the text is entered.
  - When an incorrect spelling is entered the card will flash red and the the input text will be cleared for the user to try again.
  - When the correct spelling is entered the card will flash green, the card content will be set to the next card and the words remaining will decrease by one.
  - When the are no more words remaining the final quiz finished flashcard is shown.

#### Test Case 16: Spelling quiz test functionality

- **Objective**: Verify that test specific functionality for spelling quiz works correctly.
- **Steps:**
  - Check all the scores for the words in the set about to be tested.
  - Ajust the setting in the quiz modal to be for the spelling quiz type and practice mode to be off.
  - Click the 'Start Quiz' button
  - Enter the incorrect spelling in the input field, click the check button and observe results.
  - Enter the correct spellings in the input field, click the check button and observe results, repeat with correct spelling until the quiz is finished.
  - Repeat the process but entering incorrect spellings instead.
  - Check the word scores after every quiz attempt.
- **Expected Results:**
  - When the quiz is accessed the input fields are displayed without the correct answer as a hint.
  - When the correct spelling is entered and is check it moved to the next card and decrements the words remaining by one.
  - The same happens now when entering an incorrect score.
  - After the test was run using all correct answers all the spelling scores for the words in the set tested have been incremented by 20.
  - After the test was run using all incorrect answers all the spelling scores for the words in the set tested have been decremented by 5.

#### Test Case 17: Menu mobile functionality

- **Objective**: Verify that the main navigation menu works correctly on mobile mode
- **Steps:**
  - Log into the application on a mobile device.
  - Click the menu hamburger icon button.
  - Click the close button.
  - Reope the menu.
  - Click anywhere off the menu.
- **Expected Results:**
  - When the mobile application is visited the menu drawer should not be visible by default.
  - Then the menu button is clicked the menu should expand to become visible.
  - When the close button is clicked the menu should close and no longer be visible.
  - When the menu is open and anywhere on the screen not in the menu element it clicked the menu should also close and no longer be visible.

#### Test Case 18: Tour hints

- **Objective**: Verify that the tour messages are shown to new users and can be disabled correctly.
- **Steps:**
  - Sign up for a new account and navigate.
  - Navigate to the home page and check that the tour message for the page is displayed.
  - Click the close button for the tour message.
  - Refresh the page and check the message is no longer displayed.
  - Check this for ever page or element that has a tour message asscociated with it.
- **Expected Results:**
  - When the page is loaded the tour messaged is shown.
  - When the close button is clicked the tour message is hidden and the display value for that tour message is updated in the database.

### User Testing

Exstensive user testing was carried out by letting multiple alpha-testers use the app for a number of weeks while development was taking place. They all used numerous different devices spanning mobility, browsers used and device age. The users where all selected for being diverse in their own personal traits to ensure a wide spectrum of people could use the app effectively and bug free.

I personally also tested the app on as many devices and I could following the above test cases.

For the admin based functioanlity which is solely compromised of forms I tested this manually by entering incomplete and incorrect information into the forms and ensured to invalid data was able to get through to the database following the test cases outlined above.

### Lighthouse Testing

Below are the Lighthouse Scores for every page

#### Home Page

![Lighthouse Score Home](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/lh-home.png)

#### Alphabet Page

![Lighthouse Score Alphabet](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/lh-alphabet.png)

#### Word Sets Page

![Lighthouse Score Sets](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/lh-sets.png)

#### Word List Page

![Lighthouse Score List](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/lh-list.png)

#### Flashcard Quiz Page

![Lighthouse Score Flashcard](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/lh-flashcard.png)

#### Spelling Quiz Page

![Lighthouse Score Spelling](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/lh-spelling.png)

### Known Bugs

- Flashcard flip on Safari on mobile - there is currently still some issues with the card flip animation on Safari on mobile, I've tried multiple suggested approaches to fix this to no avail. If I can't find a solution that works I will just revert to disable the flip animation on Safari Mobile and just make the card transition the front/back.

## Credits

### Icons

All icons where sourced from The Noun Project under the Creative Commons License, individual icon credits are listed below

- chevron by Landan Lloyd from <a href="https://thenounproject.com/browse/icons/term/chevron/" target="_blank" title="chevron Icons">Noun Project</a> (CC BY 3.0)
- Close by Genius Icons from <a href="https://thenounproject.com/browse/icons/term/close/" target="_blank" title="Close Icons">Noun Project</a> (CC BY 3.0)
- translate by silvio rebelo from <a href="https://thenounproject.com/browse/icons/term/translate/" target="_blank" title="translate Icons">Noun Project</a> (CC BY 3.0)
- Travel by Adrien Coquet from <a href="https://thenounproject.com/browse/icons/term/travel/" target="_blank" title="Travel Icons">Noun Project</a> (CC BY 3.0)
