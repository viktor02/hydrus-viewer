# Hydrus Viewer

## Why

When I started this project, it seemed to me that there were no good and simple solutions for the hydrus web gallery. Those that were, took time to set up and I didn't like them. So I decided to write my own gallery.

## Features

1. Search the gallery by tags
2. View images 
3. Import URLs to hydrus
4. Optimized for PC and mobile
5. Simply to install and set up.

## How to install


### Build from sources:

1. Clone the repository 

   `git clone https://github.com/viktor02/hydrus-viewer`

2. cd to cloned directory 

   `cd hydrus-viewer`

3. Install from source 

    `pip install .`

4. Run

    `hydrus_viewer <access_key>`

5. App will start at 127.0.0.1:8020 (you can change IP and Port with --bind and --port args)

### Docker

1. Clone git repo

   `git clone https://github.com/viktor02/hydrus-viewer`

2. Build with docker:

   `docker build -t hydrus_viewer ./hydrus_viewer`

3. Start containers

Using docker-compose:
```yaml
version: '3.8'
services:
  hydrusclient:
    image: ghcr.io/hydrusnetwork/hydrus:latest
    container_name: hydrusclient
    restart: unless-stopped
    environment:
      - UID=1000
      - GID=1000
    volumes:
      - ./db:/opt/hydrus/db
    tmpfs:
      - /tmp #optional for SPEEEEEEEEEEEEEEEEEEEEEEEEED and less disk access
    ports:
      - 5800:5800   #noVNC
      - 5900:5900   #VNC
      - 45868:45868 #Booru
      - 45869:45869 #API
  hydrus_viewer:
    image: hydrus_viewer
    container_name: hydrus_viewer
    restart: unless-stopped
    environment:
      - TOKEN=secrettokenforapi
      - API_URL=http://hydrusclient:45869/
      - BIND=0.0.0.0
      - PORT=80
    ports:
      - 80:80
```

## How it looks

![MainPage](img/main_page.png)
![SearchPage](img/search_page.png)
