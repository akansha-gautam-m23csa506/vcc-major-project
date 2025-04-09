FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy app code
COPY . /app

# Install dependencies
RUN pip install flask psycopg2-binary

# Expose the Flask port
EXPOSE 5000

# Run the app
CMD ["python", "main.py"]
