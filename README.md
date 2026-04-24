# oeuvre (in development!)

## What is **oeuvre**?

**oeuvre** is a personal archive for people interested in art and art history. You can save and organise works you've encountered, across categories like paintings, sculptures, photographs and architecture, all in one place.
The backend is built with Django and Django REST Framework. A React frontend is planned.

## Features

- **Multi-category art management** - paintings, sculptures, photography, architecture, and a generic "other" category
- **Full CRUD** - create, read, update, and delete art pieces per category
- **Image handling** - upload and manage multiple images per art piece
- **Filtering & search** - filter art pieces by category, year, location, artist, and more
- **[Search engine](https://github.com/dnl07/SearchEngine) integration** - art pieces are automatically indexed for full-text search on create/update/delete


## Installation

```bash
git clone --recurse-submodules https://github.com/dnl07/oeuvre.git

docker compose up --build

cp .env.example .env
```

API docs are available at ```/api/docs``` once the server is running.

## API Endpoints

### Art pieces

| Method | Endpoint | Description |
| :--- | :--- | ---: |
| GET | `/api/art-pieces` | Retrieve a list of all art pieces |
| POST | `/api/art-pieces/{category}` | Create a new art piece |
| GET | `/api/art-pieces/{category}/{id}` | Retrieve a specific art piece |
| PATCH | `/api/art-pieces/{category}/{id}` | Update a specific art piece |
| DELETE | `/api/art-pieces/{category}/{id}` | Delete a specific art piece |
| POST | `/api/art-pieces/{category}/{id}/images` | Upload images for an art piece |
| DELETE | `/api/art-pieces/{category}/{id}/images/{image_id}` | Delete an image from an art piece |

Available categories are: `painting`, `sculpture`, `photography`, `architecture` and `other`.