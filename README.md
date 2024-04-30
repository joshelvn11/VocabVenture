# VocabVenture

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

### Quiz

#### Flashcard Quiz

#### Spelling Quiz

### Scoring

### Admin Editing

### Progressive Web App

VocabVenture is also a progresive web app which improves performance and allows users to install it like a native app on mobile devices for a greatly enhaces user exeperience.

## API

## Database

### Schema

![VocabVenture Database ERM](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/vocab-venture-erm.png)

[View the ERM on Figma here](https://www.figma.com/file/Zhc99JR3FgcUm0Vguyzy6w/Vocab-Venture-ERM?type=whiteboard&node-id=0%3A1&t=aZP744msjxiJwk40-1)

## Design

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

### Object Storage

The app uses Wasabi's S3 compatable storage platform for all object based storage.

## Future Ideas / Roadmap

### AI Chat

### Phrase Library

### Multiple Languages

This entails rewriting some of the application logic to dynamically generate UI components based on the target languages data model based on what data needs to be included about the target language. For example languages the use the Roman alphabet would not need an alphabet section or to show the romanised for of words.

## Testing

### Validator Testing

### Unit Testing

All Django views are tested extensively using Django's in built unit testing framework. Multiple test cases are carried out for every view function testing for factors such as authorisation, correct responses, data validity and correct template rendering.

During unit tests a seperate Postgres test database is created on Neon and used for testing purposes where it is then destroyed at the end of every test run.

### User Testing

Exstensive user testing was carried out by letting multiple alpha-testers use the app for a number of weeks while development was taking place. They all used numerous different devices spanning mobility, browsers used and device age. The users where all selected for being diverse in their own personal traits to ensure a wide spectrum of people could use the app effectively and bug free.

### Lighthouse Testing

### Known Bugs

- Flashcard flip on Safari on mobile - there is currently still some issues with the card flip animation on Safari on mobile, I've tried multiple suggested approaches to fix this to no avail. If I can't find a solution that works I will just revert to disable the flip animation on Safari Mobile and just make the card transition the front/back.

## Credits

### Icons

All icons where sourced from The Noun Project under the Creative Commons License, individual icon credits are listed below

- chevron by Landan Lloyd from <a href="https://thenounproject.com/browse/icons/term/chevron/" target="_blank" title="chevron Icons">Noun Project</a> (CC BY 3.0)
- Close by Genius Icons from <a href="https://thenounproject.com/browse/icons/term/close/" target="_blank" title="Close Icons">Noun Project</a> (CC BY 3.0)
- translate by silvio rebelo from <a href="https://thenounproject.com/browse/icons/term/translate/" target="_blank" title="translate Icons">Noun Project</a> (CC BY 3.0)
- Travel by Adrien Coquet from <a href="https://thenounproject.com/browse/icons/term/travel/" target="_blank" title="Travel Icons">Noun Project</a> (CC BY 3.0)
