# SceneIQ Docker Setup Installation Instructions

## Prerequisites
- Docker and Docker Compose installed on your system
- Git (to clone the repository)

## Installation Steps

### 1. Clone Your SceneIQ Repository
```bash
git clone <your-repository-url>
cd <repository-directory>
```

### 2. Set Up the Docker Environment
The Docker configuration files are organized in the `docker` directory:
- `docker-compose.yml` - Main configuration file
- `Dockerfile` - Application container definition
- `.env.example` - Template for environment variables
- `init-scripts/` - Database initialization scripts
- Other utility scripts and configuration files

### 3. Configure Environment Variables
```bash
cd docker
cp .env.example .env
```
Then edit the `.env` file with your actual database credentials, API keys, and other settings:
```
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@db:5432/sceneiq
PGHOST=db
PGUSER=postgres
PGPASSWORD=postgres
PGDATABASE=sceneiq
PGPORT=5432

# API Keys
GOOGLE_API_KEY=your_google_api_key_here

# Optional: Anthropic API Key (if using Claude for AI features)
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 4. Start the Application
```bash
# Make the script executable if needed
chmod +x sceneiq-docker.sh

# Start the services
./sceneiq-docker.sh start
```

Alternatively, you can use Docker Compose directly:
```bash
docker-compose up -d
```

### 5. Access the Application
- Dashboard: http://localhost:5000
- API: http://localhost:5001
- API Documentation: http://localhost:5001/docs

## Production Deployment

For production deployment, use the production Docker Compose file:
```bash
docker-compose -f docker-compose-production.yml up -d
```

This configuration includes:
- NGINX for SSL termination
- Container health checks
- Resource limits
- Automatic restart policies

Be sure to set up SSL certificates as described in the `README-SSL.md` file before deploying to production.

## Managing the Application

The `sceneiq-docker.sh` script provides commands for common operations:
```bash
./sceneiq-docker.sh start    # Start all services
./sceneiq-docker.sh stop     # Stop all services
./sceneiq-docker.sh restart  # Restart all services
./sceneiq-docker.sh logs     # View logs from all services
./sceneiq-docker.sh status   # Check status of all services
./sceneiq-docker.sh clean    # Remove all containers and volumes
```

## Backup and Restore

Use the provided scripts for database backup and restoration:
```bash
cd docker/scripts
./backup.sh                   # Create a database backup
./restore.sh <backup-file>    # Restore from a backup file
```

## File Structure
```
docker/
├── docker-compose.yml           # Main Docker Compose configuration
├── docker-compose-production.yml # Production-ready configuration
├── Dockerfile                   # Application container definition
├── .dockerignore                # Files to exclude from Docker build
├── .env.example                 # Environment variables template
├── README.md                    # Documentation
├── README-SSL.md                # SSL setup instructions
├── requirements.txt             # Python dependencies
├── sceneiq-docker.sh            # Management script
├── update-requirements.sh       # Script to update requirements.txt
├── init-scripts/                # Database initialization
│   ├── 01-schema.sql            # Database schema creation
│   └── 02-sample-data.sql       # Sample data population
├── nginx/                       # NGINX configuration for production
│   └── conf/
│       └── sceneiq.conf         # NGINX virtual host config
└── scripts/                     # Utility scripts
    ├── backup.sh                # Database backup script
    ├── restore.sh               # Database restoration script
    └── initialize.sh            # Environment initialization script
```

## Troubleshooting

If you encounter issues:
1. Check the logs: `./sceneiq-docker.sh logs`
2. Verify your environment variables in the `.env` file
3. Ensure ports 5000 and 5001 are available on your system
4. Check that Docker and Docker Compose are properly installed

For more details, refer to the `README.md` file in the Docker directory.