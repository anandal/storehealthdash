# Integrating Docker into SceneIQ

This guide explains how to integrate the Docker configuration into your SceneIQ codebase.

## Step 1: Prepare Your Repository

Make sure you have the most up-to-date version of your SceneIQ code:

```bash
# Ensure you're at the root of your repository
cd /path/to/your/sceneiq/project
```

## Step 2: Copy Docker Configuration Files

Copy all Docker configuration files to your repository:

```bash
# Create any missing directories
mkdir -p docker/init-scripts
mkdir -p docker/nginx/conf
mkdir -p docker/scripts

# Copy all the Docker files from the provided setup
cp -r /path/to/docker/* docker/
```

## Step 3: Verify Required App Files

Ensure these key application files are present:
- `app.py` - Main Streamlit application
- `basic_api.py` - REST API implementation
- `database.py` - Database schema and connection management

## Step 4: Configure Database Connection

Update your application to use the Docker PostgreSQL database:

1. In your database connection code, check for an environment variable:

```python
# Example snippet for database.py
import os
from sqlalchemy import create_engine

# Get DATABASE_URL from environment variable, or use the default if not set
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/sceneiq")

# Create database engine
engine = create_engine(DATABASE_URL)
```

## Step 5: Test Deployment

Test your Docker deployment locally:

```bash
cd docker
cp .env.example .env
# Edit .env file with necessary credentials

# Start the Docker containers
docker-compose up -d

# Verify the containers are running
docker-compose ps

# Check the logs if needed
docker-compose logs -f
```

## Step 6: Verify Application

Access your application to ensure it's working:
- Dashboard: http://localhost:5000
- API: http://localhost:5001
- API Documentation: http://localhost:5001/docs

## Additional Configuration

For more advanced configuration options and production deployment, refer to:
- `docker/README.md` - General documentation
- `docker/README-SSL.md` - SSL configuration
- `docker-setup-instructions.md` - Detailed setup instructions