FROM python:3.9
WORKDIR /app

COPY flask_app/ /app/
COPY models/vectorizer.pkl /models/vectorizer.pkl

RUN pip install -r requirements.txt


EXPOSE 5000

CMD ["gunicorn","-b","0.0.0.0:5000","app:app"]

