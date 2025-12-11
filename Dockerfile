# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc build-essential

# Copy requirements
COPY requirements.txt .

# Upgrade pip and install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the backend code
COPY . /app

# Expose port
EXPOSE $PORT

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]
