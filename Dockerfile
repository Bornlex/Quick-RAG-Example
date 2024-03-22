FROM python:3.12
WORKDIR /app

RUN mkdir src
COPY requirements.txt main.py .env ./
COPY src/* ./src/
RUN pip install -r ./requirements.txt
ENV FLASK_ENV production

EXPOSE 5000
CMD ["gunicorn", "-b", ":5001", "main:app"]
