# SceneIQ Docker Quickstart Guide

This guide provides simple instructions for deploying your SceneIQ dashboard using Docker.

## Prerequisites
- Docker and Docker Compose installed on your system

## Quick Start Steps

### 1. Set Up Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your actual credentials
# nano .env
```

### 2. Start the Docker Environment
```bash
# Build and start the containers
docker-compose up -d

# Check the status of the containers
docker-compose ps
```

### 3. Access Your Application
- Dashboard: http://localhost:5000
- API: http://localhost:5001
- API Documentation: http://localhost:5001/docs

### 4. View Logs (Optional)
```bash
# View logs from all services
docker-compose logs -f

# View logs from a specific service
docker-compose logs -f app
docker-compose logs -f db
```

### 5. Stop the Environment
```bash
docker-compose down
```

### 6. Clean Up (If Needed)
```bash
# Remove containers, networks, and volumes
docker-compose down -v
```

## Important Files
- `docker-compose.yml` - Main Docker Compose configuration
- `Dockerfile` - Application container definition
- `.env.example` - Template for environment variables
- `docker/init-scripts/` - Database initialization scripts

## Database Initialization
The PostgreSQL database will be automatically initialized with the schema and sample data from the scripts in the `docker/init-scripts/` directory.

## Troubleshooting

If you encounter issues:
1. Check the container logs as shown above
2. Verify your environment variables in the `.env` file
3. Ensure ports 5000 and 5001 are available on your system

For more detailed configuration options, refer to the documentation in the `docker/` directory.