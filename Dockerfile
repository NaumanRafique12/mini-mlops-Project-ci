# Use a smaller base image (Alpine is more lightweight than slim)
FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Install necessary dependencies
# Combining commands into one layer

# Copy application code
COPY flask_app/ /app/
COPY models/vectorizer.pkl /app/models/vectorizer.pkl 

RUN apk add --no-cache --virtual .build-deps \
    gcc musl-dev libffi-dev \
    && pip install --no-cache-dir Flask gunicorn -r requirements.txt \
    && python -m nltk.downloader stopwords wordnet \
    && apk del .build-deps

# Expose port 5000 for the app
EXPOSE 5000

# Command to run the application with gunicorn
CMD ["gunicorn","-b","0.0.0.0:5000","python", "app:app"]
