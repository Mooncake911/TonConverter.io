FROM python:3.11

MAINTAINER vadimnodle

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade setuptools

RUN pip install --no-cache-dir -r requirements.txt

COPY ../../venv .

# Run app.py when the container launches
ENTRYPOINT ["python3", "main.py"]
