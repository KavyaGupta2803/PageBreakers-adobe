# Use Python base image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir pymupdf

# Create output directory in case it doesn't exist
RUN mkdir -p output

# Run the script
CMD ["python", "main.py"]
