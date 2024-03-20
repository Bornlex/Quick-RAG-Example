FROM python:3.12
WORKDIR /app

COPY requirements.txt main.py ./
RUN pip install -r ./requirements.txt
ENV FLASK_ENV production

EXPOSE 5000
CMD ["gunicorn", "-b", ":5000", "main:app"]
