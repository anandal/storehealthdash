#!/bin/bash

# SceneIQ Docker Environment Initialization Script
# This script prepares the Docker environment for the SceneIQ platform

echo "Initializing SceneIQ Docker environment..."

# Create necessary directories
mkdir -p backups
mkdir -p docker/nginx/ssl

# Set correct permissions for scripts
chmod +x sceneiq-docker.sh
chmod +x scripts/backup.sh
chmod +x scripts/restore.sh

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit the .env file with your actual configuration values."
else
    echo ".env file already exists."
fi

# Check for SSL certificates
if [ ! -f nginx/ssl/sceneiq.crt ] || [ ! -f nginx/ssl/sceneiq.key ]; then
    echo ""
    echo "No SSL certificates found."
    echo "For development/testing, you can generate self-signed certificates with:"
    echo ""
    echo "openssl req -x509 -nodes -days 365 -newkey rsa:2048 \\"
    echo "  -keyout nginx/ssl/sceneiq.key \\"
    echo "  -out nginx/ssl/sceneiq.crt \\"
    echo "  -subj \"/C=US/ST=State/L=City/O=Organization/CN=sceneiq.example.com\""
    echo ""
    echo "For production, please use proper certificates from a trusted CA."
    echo "See README-SSL.md for detailed instructions."
fi

echo ""
echo "Initialization complete!"
echo ""
echo "Next steps:"
echo "1. Edit the .env file with your configuration"
echo "2. Configure SSL certificates if needed"
echo "3. Start the application with ./sceneiq-docker.sh start"
echo ""
echo "For more information, see the README.md file."