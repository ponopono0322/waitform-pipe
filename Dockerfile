FROM pytorch:1.9.0-cuda10.2-cudnn7-devel
# FROM python:3.8
COPY . /app/waitform-pipe

WORKDIR /app/waitform-pipe

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "bash", "run.sh" ]