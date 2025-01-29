# FastAPI-ToDo
Small app for ToDo day tasks

## Description
Project:
- **Backend**: FastAPI
- **Frontend**: Jinja2
- **Database**: PostgreSQL

---

## Requirements

- Docker
- Docker Compose

---

## How to start the project

1. Clone repository:
   ```bash
   git clone <repository_url>
   cd FastAPI-ToDo
    ```

2. Start docker-compose
``` 
docker-compose up -d
```
3. If you change something in the project:
```commandline
docker-compose down
docker-compose up -d --build
```