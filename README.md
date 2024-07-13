# Spotipy-random-player

## Description
This is my early Python project for playing Spotify songs from command line. 

The idea is to define a list of songs one wants to learn. The songs will be played randomly from the list based on their priority (the higher the priority is, the more frequently the song appears). 

The app plays songs in a loop (control commands are printed into the console). Anytime after the songs starts playing, the user may stop it, which displays its author and name. The user may then decide whether to increase the song priority or decrease it (if they guessed it or not). And that's it!

## Setup instructions

1. Clone the repository, install python and packages listed on the top of the main file.
2. [Optional] Define your list of songs (or use the default one). The songs should be written in csv format delimited by semicolon*;* as follows: <songname>;<author>;priority
3. Rename *SAMPLE.env* file to *.env* and replace its variables with your spotify variables obtained according to the instructions: https://developer.spotify.com/documentation/web-api
4. Run the app and enjoy

## Repository information

Techstack: Python, spotipy

Author: Michael Koudela
