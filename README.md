
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
- View channels and their videos from the main page.

## Installation
### Docker Compose (Recommended)
With docker installed, make a compose file\
`docker-compose.yaml`:
```
version: "3"
services:
  tubarr:
    image: teknicallity/tubarr:latest
    ports:
      - "3020:3020"
    restart: always
    volumes:
      - ./config:/etc/tubarr/config
      - ./media:/etc/tubarr/media
```

### Docker Run
With docker installed, run
```
docker run\
    -p 3020:3020\
    -v ./config:/etc/tubarr/config\
    -v ./media:/etc/tubarr/media\
    teknicallity/tubarr:latest
```

## Usage

- Channels and Videos can be quickly viewed by the sidebar links.
- Channels have different sections: home for recent content, videos, and playlists.
- Navigate to "Add Content" in the upper right.
- This input can take either a YT video or playlist, displaying the information for either.
- Once previewed, choose download in order to have the server download the content.
- The video will be downloaded momentarily if it is the only item in queue.


## Planned Features

- Multiple content entry selection with actions
- A visible settings page
- Yt-dlp cookie detector. Currently, if there is a file `ccokies.txt` under config/ytdlp, it will be passed to yt-dlp as the YouTube cookies.

## Development
1. Make sure python 3.11 and pip are installed
2. Clone this repository
3. In the project directory, run ```pip install -r requirements.txt```
4. Then run ```python3 manage.py migrate```
5. To run the consumer ```python3 manage.py djangohuey```
6. In another terminal, run ```python3 manage.py runserver```
7. Visit "http://localhost:8000/"

## Screenshots

![Home Page](./documentation/screenshots/home-page.png?raw=true "Home Page")
![Add Page](./documentation/screenshots/add-page.png?raw=true "Add Page")
![Channel Page](./documentation/screenshots/channel-page.png?raw=true "Channel Page")
![Video Page](./documentation/screenshots/video-page.png?raw=true "Video Page")