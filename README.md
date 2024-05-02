# VocabVenture

![Device Mockups](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/device-mockup.png)

VocabVenture is language learning web app that currently supports learning Ukrainian from English. The app is designed to be easy, simple and straightforward to use with a focus around learning via repition and usage in practical examples. I created the app in response to my dislike over the many "over-gamified" solutions (such as Duolingo) where I felt my brain nor memory was not being properly strained to create new neural pathways to properly cement any word into my vocabulary and therefore not making any substantial progress at the end of the day to actually learning a new language.

VocabVenture adopts the old-fashioned but effective approach of learning through constant testing and repition and is aimed towards people like myself who prefer this method of learning. The basis of the app is having an extensive word list with crucial information needed to understand each word, its meaning, appropriate usage and semantic and gramatical nuances. While the information on each word is fairly extensive most of it is optional as while it will help further understanding of the word it is not necessary to gain the most basic and therefore practical understanding of the word. The app has been designed in such away when detailed information is initially hidden as not to overwhelm a user but easily available if they do choose to engage in depth.

## Backend

The backend of the application is built with Django. For the most part pages are server side rendered with some further client side updates being carried out using the application's REST API built using the Django's Rest Framework. Updates to database data are made the client via the REST API. Certain incremental jobs are carried out a cron job on a seperate server that makes request to certain endpoints to execute job functions (for example streaks being reset and midnight every night.)

## The Layout & Structure

### Home

The home screen is the primary entry point into the application and displays overall stats and statistics for the current user including streaks, overall progress and the learning stages of all words that the user has started learning.

### Alphabet

The alphabet is just a simple page showing the Cyrillic alphabet with the approximated English pronounciations for constant reference when learning.

### Words

The Words page is the center focal point of the application and shows a list of categorised sets of words. For each set the current logged in user's score are shown for the set. Clicking on any set will display a list of all the words contained within that set as cards with the word in the target language being the card title and underneath some basic essential information about that word including the translation, romanisationa and pronouncation.

Clicking on any word will bring up a modal displaying further detailed information on the target word including a definition, explanation and practical usage example that are interactable. Hovering (clicking on mobile) on any word in the usage example will show the contextual translation and romanisation and tooltips and underneath a show translation button can be clicked to show the translation of the sentence as a whole. This allows a learner to understand direct translation of words in their context while still not losing the overall meaning of is try to be communicated. The usage example are dynamically generated from JSON data stored in the database making it easier for an admin to easily create new interactable using examples simply by following the JSON data format.

## Features & Functions

### Intro Tour Messages

To increase UX and usability every page and feature has a message displayed explaining the page/feature including what it is and how to use it. Once the message has been closed by the user it will not be displayed again by persisting the state of the message for that specific user to the database.

### Home Screen & Stats

The main entry point of the app is the home screen where can see various stats related to their account including:

1. Quiz Current Streak - how many days in a row have they have taken a test quiz for each respective quiz type.
2. Quiz Longest Streak - what their longest recorded streak was for each respective quiz type.
3. Word Progress - their overall word progress for all the words in the app. This shows the progress of how many words they have a score for out of all the overall words in the app broken down and color coded by amount of words in each learning stage (New, Learning, Learnt, Mastered)
4. Learning Stage Breakdown - these are seperate cards show the percentage of words the user has scores for in each learning stage.

![Home Screen Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/home-screen.png)

### Alphabet

This is a full list of letters in the Cyrillic alphabet showing approximate pronounciations for each letter.

![Alphabet Screen Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/alphabet.png)

### Word Sets

In the app all words are divided up into sets for easier and more structured learning, words can be in multiple sets. The sets page displays these sets and allow users to navigate to the page containing all words in that set by clicking on the set item. The sets also show stats for the user scores in each specific set. It shows the average score of all the words broken down by quiz type and the overall word score.

![Word Sets Screen Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/word-sets.png)

### Word Lists

The word list page displays a list of the words in the respective set that was accessed. Earch word is displayed as a card with the word in Ukrainian as the main card element and the most basic and essential info about the word including the English translation, romanization and pronounciation. It also display a progress bar show the overall word score progress for the word which is an average of the three quiz scoring metrics. By clicking on a word a modal is displayed showing further details about the word.

When the word list is accessed this page is always dynamically generated however the extended word details are also loaded in behind the seens via and API call to the server on page load. This reduces database requests and speeds up performance when the word details modal is shown.

![Word List Screen Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/word-list.png)

### Word Details

The word details modal can be accessed by clicking on any word in the word list screen. Clicking on a word with open this modal which shows further information about the word be accessed. The data in the modal is dynamically generated from the data loaded from the API in the previous step. The word details modal also contains the relevant score data for the various quiz types of the current word being viewed. Clicking the audio button at the top allows the user to hear the pronounciation of the current word.

![Word Details Screen Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/word-details.png)

### Usage Examples

The usage examples are interactive element of the word details modal where users can see the word in the context of an actual Ukrainian sentence. Hovering over any word in the sentence allows the user to see the romanisation of that word and the direct translation of the word in the context of the current sentence. Clicking the 'Show Translation' button underneath the sentence will show the overall translation of that sentence.

The interactive usage examples are dynamically generated from data stored as JSON when then the modal is opened. Storing the data as JSON and creating an automatic rendering process for the interactions makes it very simple for non-technical admins to create these interactable elements.

![Usage Examples Screen Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/usage-examples.png)

### Quiz

The quiz component of the app is probably the most integral part next to the words themselves as it is the part that allows users to practice and really improve their vocabulary.

There are currently two quiz types players can use to practice: a flashcard quiz and a spelling quiz, each of which are described in further detail below.

Furthermore each quiz type can be playes in two different modes: Practice and test mode. In practice mode questions are repeated until the user gets them right and answers are not scored meaning a correct answers does not contribute any points to a word's score and wrong answer does not deduct any points from a word's score.

Currently only the predefined word sets can be quized and this can be accessed by clicking the 'Quiz' button at the top of any set. Upon clicking the button the user is presented with a modal allowing them to select the quiz type they wish to use and whether or not to quiz in practice or test mode. When the 'Start Quiz' button is clicked the quiz is then started with the configuration they chose.

![Quiz Modal Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/quiz-modal.png)

#### Flashcard Quiz

The flashcard quiz type is probably a familiar concept to everyone. When the user opts to take a flashcard quiz two cards are generated for every word in the set, one for Ukrainian to English and one for the reverse, English to Ukrainian. These cards are then shuffled and generated into interactable card elements for the user to play with.

How it works is a card is shown with the question side facing the user, the question asking for the translation of the Ukrainian or English word depeneding on which card is being shown. The user can then flip the card and select whether they were correct or incorrect.

In practice mode if they are correct the card is removed from the deck and they proceed to the next card. If they are incorrect the card is moved to the end of the deck where they can attempt it again. This continues until all cards are correctly guessed.

In test mode the same process happens with a correct answer and their score for that word is incremented. If they get an answer incorrect in test mode the word is also removed from the deck but this time not added onto the end and their score for that word is decremented.

Once they have finished the quiz they can choose to restart or exit the quiz.

![Flashcard Quiz Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/flash-cards.png)

#### Spelling Quiz

The spelling quiz allows users to test and practice their memory and spelling while also learning the meaning of words in the context of sentence at the same time.

When the user access the spelling quiz a set of 'spelling cards' are generated for the current set, shuffled and displayed to the user. On each card is an instruction given the English translation that needs to be filled in, an interactive sentence like in the usage examples but where the focus word is there is an input field for the user to fill in the missing word. It also includes a 'Show Translation' button to show the overall translation of the sentence.

In practice mode the answer is shown as a hint for the input so the user can see the answer until they enter any character at which point the hint will disapear. Showing the answer like this and letting the user type it in may seem counter-productive but is essential for built that muscle memory for learning words. In a similar fashion to the flashcards if the user get's the answer incorrect in practice mode the card will be repeated except this time not at the end. The card is immeditaley shown again until the user gets the correct answer.

In test mode the key difference is that no word hint is shown so the user needs to remember it completely from their own memory. This rest of the test mode functionality is the same as the flashcard test mode being that questions are not repeated when incorrect and users' score are incremented/decremented if they get question correct/incorrect.

![Spelling Quiz Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/spelling-quiz.png)

### Scoring

The scoring system is fairly simple, every word has three scoring metrics:

1. Flashcard Score - the score contributed to by answering Flashcards that are Ukrainian to English
2. Flashcard Score (Reverse) - the score contributed to by answering Flashcards that are English to Ukrainian
3. Spelling - the score that is contributed to by answering spelling questions

Each word then has a total score which is the average of these score.

Every set also has the scores calculated for each user. It has each of the same three score metrics which is calculated by taking the score for each score metric for each word in the set then calculating an average of all the words in the set. The set total is then calculated by taking the sets three scores and finding the average.

In tests every correct answer increments the word score by 20 points and every incorrect answer decrements the score by 5 points.

Every word is divided into four different learning stages based on the word's score:

1. New - 0 to 24%
2. Learning - 25% to 74%
3. Learnt - 75% to 99%
4. Mastered - 100%

### Admin Editing

Admins are able to add, delete and edit word data on the front end of the app using API calls to the server. Using custom built forms on the front end and submitting data via API calls prevents the need for page reloads ultimately resulting in a better user experience.

To access word addition functionality the admin can navigate to any set where they will see the button to add a word, this button is only availale if the user is authenticated as a super user. Clicking this brings up a modal with a form with all required fields for the data necessary to create a new word object. There is also a checklist of sets that is dynamically generating by getting all the existing sets from the server via API call. Once the word is created the admin then can check (or uncheck) sets they want the word to be in. Some of the fields are prepopulated with data such as the Word ID which is a random eight digit number.

Each field is first validated on the client side and the again validated by the model's serializer on the server side. Any error in any of these validations will alert the user to the error by an alert pop up.

The user is also alerted to every successful action such as adding a word or adding the word to a set.

![Word Add Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/word-add.png)

If the admin wishes to edit the word they can navigate to the word details modal and click the edit button which will bring up the same modal but prepopulated with all the data of the current word being edited.

![Word Edit Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/word-edit.png)

### Navigation Bar

The navigation bar is designed to be simple and easy to use, it is located on the left of the screen and is always visible to the user on desktop. On mobile it collapses and a hamburger menu button becomes available to expand the menu. The menu can then be closed but hitting the close button or clicking anywhere off the menu.

The menu links are outlined and coloured using the primary colour of the application to indicate to the user which page they are currently on.

### Profile

The profile system is currently very basic and just allows the user to see they are logged in with the correct profile and log out if they need to. The profile button is located at the bottom of the navigation bar to seperate it from all the app functions and so it always accessible to the user. Clicking the profile button expands a small menu where they can see their username and email and includes a log out button to log out of the app.

### Alert Notifications

I created a custom alert notification system to show alerts to the user to update them on any import information and give them feedback about their actions or if there if any error occur.

There is a fixed container located in the upper right hand corner used to hold and display alert notifications. It operates as a stack so multiple alter notifications can be stacked on top of one another if multiple alerts occur in a short space of time.

The alert notification are split into four categories: Info, Warning, Error and Success. Each alert is colour coded and the alert will be outlined in the alert colour as well as the alert title set to the name of the alert category. This makes it easy for users to understand the purpose and intent of message.

Message can be closed manually using the close icon on each alert but will also close automatically after eight seconds.

![Alert Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/alerts.png)

### Login / Sign Up

The login and sign up system uses all Django's default authentication system functionality however I have customised the styling fairly heavily to be as user-friendly as possible and inline with the design of the rest of the application as well as also being inline the conventional login/sign up form look that users will probably be used to.

There is also a link to each alternate page the bottom of the form to allow users to easily navigate betwen each page.

![Login Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/login.png)

![Sign Up Screenshot](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/sign-up.png)

### Progressive Web App

VocabVenture is also a progresive web app which improves performance and allows users to install it like a native app on mobile devices for a greatly enhaces user exeperience. I achieved this using the Django PWA module which made it very simple to implement.

## API

For this application I created a custom REST API using Django's Rest Framework. I adopted this approach for multiple reasons firstly being while most of the site is rendered on the server I want some components to be only be rendered when necessary and prevent uncessary database calls and rendering on the server for components that may not even be used. It also allowed the client to make updates to data without having to reload pages such as when updating scores or word data. These use cases all use Django's authetication tokens to verify the access level of the user access the API. Some API endpoints are public meaning users do not have to be logged in to access them which is useful if other application wish to use the application's data.

The other purpose is for running scheduled jobs on the database such as updating user streaks at midnight every night. I had initially attempted to use celery and rabbitmq as a message broker to achieve but ran into some limitations using the approach with the hosting I was using to I instead opted to make job functions accessible as an API endpoint that are then called at set intervals by a cron job on another server, specifically I have use cron-job.org to accomplish this. These job requests are authenticated using a secret access token as a parameter when making requests.

## Database

### Schema

![VocabVenture Database ERM](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/vocab-venture-erm.png)

[View the ERM on Figma here](https://www.figma.com/file/Zhc99JR3FgcUm0Vguyzy6w/Vocab-Venture-ERM?type=whiteboard&node-id=0%3A1&t=aZP744msjxiJwk40-1)

## Design

The design of the app is focused on overall simplicity and useability for the best overall user experience. It adopts a mainly card based design to easily segment information into manageable and identifiable chunks to make the information easier to consume and generally less overwhelming. It follows a fairly conventional design approach adopted by many other popular apps and websites to ensure it is easy and inituiative to user for all levels of users.

The app design is general was developed from a mobile first approach to ensure mobile users were considered as the primary users and to make the mobile experience as best as possible.

The colours are kept simple as well using black and white for most of the app and highlight specific important elements using the primary colour where needed. Buttons also show their level of importance by using either a solid background or white background with a border to denote the significance and priority of the button.

You will also notice subtle yet valuable animations all over the app to give immediate feedback to the user's about the state and result of their interactions with the app.

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
4. Add necessary evironment variables for the database URL, disable collectstatic value and the job secret key (use for running remote cron jobs).
5. Finalise the creation.
6. The web service will now deploy from the Github repo and on every subsequent push to the repo.

### Database

The database is a Postgresql database also running using Render which automates the process of database deployment and management.

### Object Storage

The app uses Wasabi's S3 compatable storage platform for all object based storage.

## Future Ideas / Roadmap

### AI Chat

### Phrase Library

### Multiple Languages

This entails rewriting some of the application logic to dynamically generate UI components based on the target languages data model based on what data needs to be included about the target language. For example languages the use the Roman alphabet would not need an alphabet section or to show the romanised for of words.

## Testing

### Validator Testing

#### W3C HTML Validator

The HTML unfortunately did pass through the validator with a few errors however most where necessary foy the application to work and are not critical nor inhibit function in any way, for example I have error that the letter-id or word-id attribute is not allowed on a div element but this was my method for retrieving data from the DOM element to know what word to display details for on the word details modal when it is shown.

There were also a couple error related to certain sizes not being set on link elements to do with PWA icons however these are auto-generated by Django and I couldn't seem to find a way to edit them directly.

#### Jigsaw CSS Validator

The CSS passed through the validator with no errors.

### Unit Testing

All Django views are tested extensively using Django's in built unit testing framework. Multiple test cases are carried out for every view function testing for factors such as authorisation, correct responses, data validity and correct template rendering.

During unit tests a seperate Postgres test database is created on Neon and used for testing purposes where it is then destroyed at the end of every test run.

### User Testing

Exstensive user testing was carried out by letting multiple alpha-testers use the app for a number of weeks while development was taking place. They all used numerous different devices spanning mobility, browsers used and device age. The users where all selected for being diverse in their own personal traits to ensure a wide spectrum of people could use the app effectively and bug free.

For the admin based functioanlity which is solely compromised of forms I tested this manually by entering incomplete and incorrect information into the forms and ensured to invalid data was able to get through to the database

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
