FROM python:2.7

RUN pip install beautifulsoup4

RUN pip install html5lib

RUN pip install -U nltk

RUN pip install scrapy

EXPOSE 6023 6023
