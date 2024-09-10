# Stage 1: Build Stage
FROM python:3.11.9-slim AS build
WORKDIR /app
# Copy the requirements.txt file from the flask_app folder COPY flask_app/requirements.txt /app/
# Install dependencies
COPY flask_app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
# Copy the application code and model files
COPY flask_app/ /app/
COPY models/vectorizer.pkl /app/models/vectorizer.pkl
COPY reports/versions.json /app/reports/versions.json

RUN pip install gunicorn && python -m nltk.downloader stopwords

# Stage 2: Final Stage
FROM python:3.11.9-slim AS final
WORKDIR /app
COPY --from=build /app /app
# Copy only the necessary files from the build stage COPY --from-build /app/app
# Expose the application port
EXPOSE 5000
CMD ["gunicorn","-b","0.0.0.0:5000","app:app"]