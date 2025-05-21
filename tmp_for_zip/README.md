# SceneIQ Docker Deployment

This directory contains all necessary files to deploy the SceneIQ dashboard and API using Docker.

## Prerequisites

- Docker
- Docker Compose
- Environment variables or .env file (see .env.example)

## Quick Start

1. Copy the .env.example file to .env and fill in your environment variables:
   ```
   cp .env.example .env
   ```

2. Start the application:
   ```
   docker-compose up -d
   ```

3. Access the applications:
   - Dashboard: http://localhost:5000
   - API: http://localhost:5001
   - API Documentation: http://localhost:5001/docs

## Environment Variables

The following environment variables are required:

- `DATABASE_URL`: PostgreSQL connection string
- `PGHOST`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`, `PGPORT`: PostgreSQL connection details
- `GOOGLE_API_KEY`: API key for Google AI services (if using AI assistant features)

## Components

- **app**: Main SceneIQ application container running both Streamlit dashboard and FastAPI
- **db**: PostgreSQL database for storing application data

## Data Persistence

Data is persisted in a Docker volume named `postgres_data`.

## Troubleshooting

- If the application fails to start, check the logs:
  ```
  docker-compose logs app
  ```

- If the database fails to start, check the logs:
  ```
  docker-compose logs db
  ```