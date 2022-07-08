FROM python:3.8

COPY . /app/API

WORKDIR /app/API

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python", "test.py" ]
