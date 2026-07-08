FROM python:slim

WORKDIR /usr/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "./main.py" ]

# https://hub.docker.com/_/postgres
# has a section initialization scripts
# *.sql and *.sh scripts in /docker-entrypoint-initdb.d are run at initialization