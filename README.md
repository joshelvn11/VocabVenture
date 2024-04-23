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

## Future Ideas / Roadmap

### Multiple Languages

This entails rewriting some of the application logic to dynamically generate UI components based on the target languages data model based on what data needs to be included about the target language. For example languages the use the Roman alphabet would not need an alphabet section or to show the romanised for of words.
