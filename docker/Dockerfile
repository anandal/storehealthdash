FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose ports
EXPOSE 5000 5001

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Entry point
CMD ["bash", "-c", "python -m streamlit run app.py --server.port=5000 --server.headless=true --server.address=0.0.0.0 & python basic_api.py"]