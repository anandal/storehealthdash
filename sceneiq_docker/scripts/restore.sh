#!/bin/bash

# SceneIQ Database Restore Script
# This script restores the PostgreSQL database from a backup file

# Check if a backup file was provided
if [ -z "$1" ]; then
  echo "Error: No backup file specified."
  echo "Usage: $0 <backup_file.sql.gz>"
  exit 1
fi

BACKUP_FILE=$1

# Check if the backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
  echo "Error: Backup file '$BACKUP_FILE' not found."
  exit 1
fi

# Load environment variables
source ../.env

echo "Starting SceneIQ database restoration..."
echo "This will overwrite the current database. Are you sure? (y/n)"
read -r confirmation

if [ "$confirmation" != "y" ] && [ "$confirmation" != "Y" ]; then
  echo "Restoration cancelled."
  exit 0
fi

# Decompress the backup file if it's compressed
if [[ "$BACKUP_FILE" == *.gz ]]; then
  echo "Decompressing backup file..."
  gunzip -c "$BACKUP_FILE" > temp_backup.sql
  UNCOMPRESSED_BACKUP="temp_backup.sql"
else
  UNCOMPRESSED_BACKUP="$BACKUP_FILE"
fi

# Execute database restoration
echo "Restoring database from backup..."
docker-compose exec -T db psql \
  -U ${PGUSER:-postgres} \
  -d ${PGDATABASE:-sceneiq} < "${UNCOMPRESSED_BACKUP}"

# Check if restoration was successful
if [ $? -eq 0 ]; then
  echo "Database restoration completed successfully."
else
  echo "Database restoration failed!"
  exit 1
fi

# Clean up temporary files
if [[ "$BACKUP_FILE" == *.gz ]]; then
  rm temp_backup.sql
  echo "Temporary files cleaned up."
fi

echo "Restoration process completed."