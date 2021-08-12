FROM python:3.9.6-slim-buster

WORKDIR /app

COPY ./app .

RUN pip3 install beautifulsoup4
RUN pip3 install flask
RUN pip3 install requests

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
