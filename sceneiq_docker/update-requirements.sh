#!/bin/bash

# Update requirements.txt file by scanning the project
# This script generates an accurate requirements.txt based on the actual imports

cd ..

echo "Updating requirements.txt from project imports..."

# Create a temporary file to store package imports
TEMP_FILE=$(mktemp)

# Find all Python files and extract import statements
find . -name "*.py" | while read -r file; do
    # Skip virtual environment directories
    if [[ $file == *"venv"* || $file == *"env"* ]]; then
        continue
    fi
    
    # Extract import statements
    grep -E "^import |^from " "$file" >> $TEMP_FILE
done

# Extract unique package names
echo "# SceneIQ requirements" > docker/requirements.txt
echo "# Generated on $(date)" >> docker/requirements.txt
echo "" >> docker/requirements.txt

# Add core packages explicitly with versions
cat << EOF >> docker/requirements.txt
# Core packages
streamlit==1.31.0
pandas==2.1.4
numpy==1.26.3
plotly==5.18.0
fastapi==0.109.2
uvicorn==0.27.0
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
pydantic==2.5.3
python-dotenv==1.0.0

# API and data handling
requests==2.31.0
aiohttp==3.9.1
httpx==0.26.0

# AI features
google-generativeai==0.3.1

# Security
python-jose==3.3.0
passlib==1.7.4
bcrypt==4.0.1

# Other utilities
pytz==2023.3
python-multipart==0.0.6
EOF

echo "Generated requirements.txt with core dependencies and explicit versions."
echo "You may need to manually add any additional dependencies specific to your project."