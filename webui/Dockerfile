FROM python:3.11-slim

WORKDIR /usr/app

COPY requirements.txt .
COPY main.py .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./main.py"]
