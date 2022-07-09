FROM --platform=linux/amd64 python:3.8

COPY . /app/Crawling

RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get update && apt-get -y install ./google-chrome-stable_current_amd64.deb

WORKDIR /app

RUN pip3 install flask
RUN pip3 install -r Crawling/requirements.txt

ENTRYPOINT [ "python", "Crawling/crawling_api.py" ]