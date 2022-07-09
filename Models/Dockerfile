FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-devel
# FROM python:3.8
COPY . /app/Models

WORKDIR /app

RUN pip3 install -r Models/requirements.txt

ENTRYPOINT [ "python", "Models/run.py", "--mode", "train" ]
