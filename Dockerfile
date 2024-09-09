# Use a smaller base image (Alpine is more lightweight than slim)
FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Install build dependencies for compiling Python packages
RUN apk add --no-cache gcc musl-dev libffi-dev

# Copy application code and model files
COPY flask_app/ /app/
COPY models/vectorizer.pkl /app/models/vectorizer.pkl 

# Install Python packages and download NLTK data
RUN pip install --no-cache-dir Flask gunicorn -r requirements.txt \
    && python -m nltk.downloader stopwords wordnet \
    && apk del gcc musl-dev libffi-dev

# Expose port 5000 for the app
EXPOSE 5000

# Command to run the application with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
