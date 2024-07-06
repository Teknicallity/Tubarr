
# Tubarr

Tubarr is a web application designed to simplify the process of archiving videos. 
Whether you want to save a single video or an entire playlist, Tubarr makes it easy. 
Built on Django and utilizing yt-dlp for downloading videos, Tubarr offers a user-friendly interface for managing and storing your favorite videos.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Planned Features](#planned-features)

## Features

- Download a single video, or a whole playlist.
- View channels and their videos from the main page

## Installation

1. Make sure python 3.11 and pip are installed
2. Clone this repository
3. In the project directory, run ```pip install -r requirements.txt```
4. Then run ```python3 manage.py migrate```
5. Finally, run ```python3 manage.py runserver```
6. Visit "http://localhost:8000/channels"

## Usage

- Once on the homepage, "http://localhost:8000/channels", you can click "Add Content" in the upper right.
- This input can take either a YT video or playlist, displaying the information for either.
- Once previewed, choose download in order to have the server download the content.
- After the page refreshes, the channel and video will be available on the home page for viewing.


## Planned Features

- The search bar is not functional.
- Currently, the application is thread limited. Either python threads or django works will be implemented.
- Multiple content entry selection with actions
- Improving the UI to be more modern
- A visible settings page

## Screenshots

![Home Page](./documentation/screenshots/home-page.png?raw=true "Home Page")
![Add Page](./documentation/screenshots/add-page.png?raw=true "Add Page")
![Channel Page](./documentation/screenshots/channel-page.png?raw=true "Channel Page")