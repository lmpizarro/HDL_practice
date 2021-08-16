# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

RUN apt-get update && apt-get install verilator wget git -y && apt-get install libevent-dev libjson-c-dev -y

RUN wget https://raw.githubusercontent.com/enjoy-digital/litex/master/litex_setup.py
RUN chmod +x litex_setup.py
RUN ./litex_setup.py init install

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "memory.py"]

