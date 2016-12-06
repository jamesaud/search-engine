FROM python:3.5

RUN apt-get update

RUN pip3 install scrapy

ADD . /myscrapy

WORKDIR /myscrapy

EXPOSE 6023 6023
