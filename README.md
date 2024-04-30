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

### Quiz

#### Flashcard Quiz

#### Spelling Quiz

### Scoring

### Admin Editing

## API

## Database

### Schema

![VocabVenture Database ERM](https://s3.eu-west-1.wasabisys.com/vocabventure/documents/vocab-venture-erm.png)

[View the ERM on Figma here](https://www.figma.com/file/Zhc99JR3FgcUm0Vguyzy6w/Vocab-Venture-ERM?type=whiteboard&node-id=0%3A1&t=aZP744msjxiJwk40-1)

## Design

### UI Design Mockup

[View the Mockup on Figma here](https://www.figma.com/file/P8PLJER8rZtrxbMYkEH8Wz/Vocab-Venture-Design?type=design&mode=design&t=cU2YagP9xr99O5fx-1)

## Deployment

The application itself is currently deployed to a Render Web Server instance and the database to a Render database instance.

The deployment process follows these steps:

1. Create a Render web service instance.
2. Select 'Deploy from Github repo'.
3. Connect the relevant repo.
4. Add necessary evironment variables for the database URL, disable collectstatic value and the job secret key (use for running remote cron jobs).
5. Finalise the creation.
6. The web service will now deploy from the Github repo and on every subsequent push to the repo.

## Future Ideas / Roadmap

### AI Chat

### Phrase Library

### Multiple Languages

This entails rewriting some of the application logic to dynamically generate UI components based on the target languages data model based on what data needs to be included about the target language. For example languages the use the Roman alphabet would not need an alphabet section or to show the romanised for of words.

## Testing

### Validator Testing

### Known Bugs

- Flashcard flip on Safari on mobile - there is currently still some issues with the card flip animation on Safari on mobile, I've tried multiple suggested approaches to fix this to no avail. If I can't find a solution that works I will just revert to disable the flip animation on Safari Mobile and just make the card transition the front/back.

## Credits

### Icons

All icons where sourced from The Noun Project under the Creative Commons License, individual icon credits are listed below

- chevron by Landan Lloyd from <a href="https://thenounproject.com/browse/icons/term/chevron/" target="_blank" title="chevron Icons">Noun Project</a> (CC BY 3.0)
- Close by Genius Icons from <a href="https://thenounproject.com/browse/icons/term/close/" target="_blank" title="Close Icons">Noun Project</a> (CC BY 3.0)
- translate by silvio rebelo from <a href="https://thenounproject.com/browse/icons/term/translate/" target="_blank" title="translate Icons">Noun Project</a> (CC BY 3.0)
- Travel by Adrien Coquet from <a href="https://thenounproject.com/browse/icons/term/travel/" target="_blank" title="Travel Icons">Noun Project</a> (CC BY 3.0)
