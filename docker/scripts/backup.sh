#!/bin/bash

# SceneIQ Database Backup Script
# This script creates backups of the PostgreSQL database used by SceneIQ

# Load environment variables
source ../.env

# Configuration
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/sceneiq_backup_${TIMESTAMP}.sql"

# Create backup directory if it doesn't exist
mkdir -p ${BACKUP_DIR}

echo "Starting SceneIQ database backup..."

# Execute database backup
docker-compose exec -T db pg_dump \
  -U ${PGUSER:-postgres} \
  -d ${PGDATABASE:-sceneiq} \
  -F p > ${BACKUP_FILE}

# Check if backup was successful
if [ $? -eq 0 ]; then
  echo "Backup completed successfully: ${BACKUP_FILE}"
  
  # Compress the backup
  gzip ${BACKUP_FILE}
  echo "Backup compressed: ${BACKUP_FILE}.gz"
  
  # Delete backups older than 30 days
  find ${BACKUP_DIR} -name "sceneiq_backup_*.sql.gz" -type f -mtime +30 -delete
  echo "Cleaned up old backups (older than 30 days)"
else
  echo "Backup failed!"
  exit 1
fi

echo "Backup process completed."