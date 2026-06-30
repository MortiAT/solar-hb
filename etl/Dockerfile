FROM python:slim

WORKDIR /usr/app

RUN apt update
RUN apt-get -y install postgresql-client # TODO probably not need after debugging is done

# COPY ./resources/requirements.txt requirements.txt

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# CMD [ "python3", "./src/main.py" ]
CMD [ "python3", "./main.py" ]

# https://hub.docker.com/_/postgres
# has a section initialization scripts
# *.sql and *.sh scripts in /docker-entrypoint-initdb.d are run at initialization