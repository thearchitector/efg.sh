FROM python:3.11

WORKDIR /app

RUN apt-get update && \
    apt-get -y install vim && \
    pip install pdm

COPY . .

RUN pdm export -G :all -o req.txt --without-hashes && \
    pip install -r req.txt

CMD [ "tail", "-f", "/dev/null" ]
