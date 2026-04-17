"""
Docker configuration for TruthLens
Run the application in containers for easy deployment
"""

# This file describes how to containerize TruthLens

## Docker Setup

### Build Images

Backend:
```bash
cd backend
docker build -t truthlens-backend .
```

Frontend:
```bash
cd frontend
docker build -t truthlens-frontend .
```

### Run Containers

Backend:
```bash
docker run -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/models:/app/models \
  truthlens-backend
```

Frontend:
```bash
docker run -p 3000:3000 truthlens-frontend
```

### Docker Compose

Create `docker-compose.yml` in root:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    volumes:
      - ./backend/uploads:/app/uploads
      - ./backend/models:/app/models
    environment:
      - FLASK_ENV=production
      - DEVICE=auto
    networks:
      - truthlens

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:5000/api
    networks:
      - truthlens
    depends_on:
      - backend

networks:
  truthlens:
    driver: bridge
```

Run all services:
```bash
docker-compose up
```

### Dockerfiles

Backend Dockerfile:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

Frontend Dockerfile:
```dockerfile
FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```
