FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-devel

COPY . /app/Models

WORKDIR /app

RUN pip3 install -r Models/requirements.txt

ENTRYPOINT [ "python", "Models/model_api.py"]
