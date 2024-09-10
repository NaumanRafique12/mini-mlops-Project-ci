# Stage 1: Build stage (install dependencies)
FROM python:3.11.9-slim AS builder

# Set working directory
WORKDIR /app

# Copy only requirements.txt first to leverage Docker cache
COPY flask_app/requirements.txt /app/requirements.txt

# Install dependencies and download NLTK data in one layer
RUN pip install --user -r requirements.txt && \
    python -m nltk.downloader stopwords wordnet

# Stage 2: Final stage
FROM python:3.11.9-slim AS runtime

# Set environment variables to avoid using root and cache
ENV PATH=/root/.local/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy only necessary app files from builder stage
COPY --from=builder /root/.local /root/.local
COPY flask_app/ /app/
COPY models/vectorizer.pkl /app/models/vectorizer.pkl
COPY reports/versions.json /app/reports/versions.json

# Expose the necessary port
EXPOSE 5000

# Command to run the app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
