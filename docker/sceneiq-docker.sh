#!/bin/bash

# SceneIQ Docker Management Script
# This script simplifies Docker operations for the SceneIQ platform

cd "$(dirname "$0")"

# Function to display usage instructions
function show_help {
    echo "SceneIQ Docker Management Script"
    echo ""
    echo "Usage:"
    echo "  ./sceneiq-docker.sh [command]"
    echo ""
    echo "Commands:"
    echo "  start        - Start all SceneIQ services"
    echo "  stop         - Stop all SceneIQ services"
    echo "  restart      - Restart all SceneIQ services"
    echo "  logs         - Show logs from all services"
    echo "  logs-app     - Show logs from the application service"
    echo "  logs-db      - Show logs from the database service"
    echo "  status       - Show status of all services"
    echo "  build        - Rebuild all services"
    echo "  clean        - Remove all containers and volumes"
    echo "  help         - Show this help information"
    echo ""
}

# Command handling
case "$1" in
    start)
        echo "Starting SceneIQ services..."
        docker-compose up -d
        echo "Services started. Access dashboard at http://localhost:5000 and API at http://localhost:5001"
        ;;
    stop)
        echo "Stopping SceneIQ services..."
        docker-compose down
        echo "Services stopped."
        ;;
    restart)
        echo "Restarting SceneIQ services..."
        docker-compose restart
        echo "Services restarted."
        ;;
    logs)
        echo "Showing logs from all services (Ctrl+C to exit)..."
        docker-compose logs -f
        ;;
    logs-app)
        echo "Showing logs from application service (Ctrl+C to exit)..."
        docker-compose logs -f app
        ;;
    logs-db)
        echo "Showing logs from database service (Ctrl+C to exit)..."
        docker-compose logs -f db
        ;;
    status)
        echo "Service status:"
        docker-compose ps
        ;;
    build)
        echo "Rebuilding SceneIQ services..."
        docker-compose build
        echo "Build complete."
        ;;
    clean)
        echo "Removing all containers and volumes..."
        docker-compose down -v
        echo "Cleanup complete."
        ;;
    help|*)
        show_help
        ;;
esac