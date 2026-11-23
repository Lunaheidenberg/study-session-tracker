# Study Session Tracker API

A simple REST API for tracking study sessions, built with Flask, Redis, and Docker Compose.

## Tech Stack

- **Flask:** REST API
- **Redis:** Stores study statistics
- **Docker & Docker Compose:** Containerization and service orchestration
- **pytest:** Automated testing

## Features

- Record study sessions
- Track total study sessions and minutes
- Redis data persistence using AOF and Docker volumes
- Redis health checks
- Automated API tests

## Prerequisites

- Docker Engine
- Docker Compose

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/Lunaheidenberg/study-session-tracker.git
   cd study-session-tracker
   ```

2. Build and start the services:

   ```bash
   docker compose up -d --build
   ```

3. Check container status:

   ```bash
   docker compose ps
   ```

The API is available at `http://localhost:5060`.

## API Endpoints

### GET /health

```bash
curl http://localhost:5060/health
```

### POST /sessions

```bash
curl -X POST http://localhost:5060/sessions \
  -H "Content-Type: application/json" \
  -d '{"minutes":45}'
```

### GET /stats

```bash
curl http://localhost:5060/stats
```

## Running Tests

Create and activate a Python virtual environment, install dependencies, then run:

```bash
python -m pip install -r requirements.txt
python -m pytest -v
```

## Data Persistence

Redis uses Append Only File (AOF) persistence and a Docker named volume. Data is preserved when containers are recreated, provided the volume is retained.

## Stop the Application

```bash
docker compose down
```

Avoid `docker compose down -v` if you want to keep stored data.