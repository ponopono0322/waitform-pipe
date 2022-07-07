FROM pytorch:1.9.0-cuda10.2-cudnn7-devel

COPY . /app/waitform-pipe

WORKDIR /app/waitform-pipe

RUN pip3 install -r requirements.txt