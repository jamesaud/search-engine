FROM python:3.5

RUN apt-get update

RUN pip3 install beautifulsoup4

RUN pip3 install html5lib

RUN pip3 install -U nltk

ADD . /project

WORKDIR /project