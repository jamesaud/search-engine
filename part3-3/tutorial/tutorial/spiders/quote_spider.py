import scrapy
import urllib.parse
from scrapy.exceptions import CloseSpider
import sys
import os


# Summary:
# So here we are sub-classing a class from scrapy and
# building a dfs search. We are using a stack data structure and backtracking
# up our link structure when we hit a limit. We found this could only be done using
# a stack. We had some minor issues on how to transfer over variables but
# solved this by reading a file.
class DfsSpider(scrapy.Spider):
    name = "dfs"
    counter = 0
    limit = 10
    directory = "/"

    def __init__(self):

        file = open('global_settings.txt', 'r')

        for index, arg in enumerate(file.readlines()):
            if index == 0:
                self.urls = [arg.strip()]
            if index == 1:
                self.limit = int(arg.strip())
            if index == 2:
                self.directory = arg.strip()

        self.visited = set()


    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):

        if self.counter >= self.limit:
            raise CloseSpider('Limit Reached')

        self._increase_counter()

        #page = response.url.split("/")[-2]
        urls = self.collect_urls(response)

        self.write_contents(response, self._get_counter())
        self.counter+=1

        for url in urls:
            if url not in self.visited:
                self.visited.add(url)
                yield scrapy.Request(url=url, callback=self.parse)


    def collect_urls(self, response):
        urls = []
        # Collect all the links in current page, append to urls
        for sel in response.xpath('//a'):
            res = sel.xpath('@href').extract()
            if not res:
                continue
            res = res[0]
            if 'http' not in res:
                res = urllib.parse.urljoin(response.url, res)
            urls.append(res)
        return urls

    def write_contents(self, response, counter):
        filename = str(counter) + '.html'
        filename = os.path.join(self.directory, filename)
        with open(filename, 'w') as f:
            f.write(str(response.body))
        self.log('Saved file %s' % filename)

        with open('index.dat', 'a') as file:
            file.write(filename + ' ' + str(response.url) + '\n')


    @classmethod
    def _increase_counter(cls):
        cls.counter += 1

    @classmethod
    def _get_counter(cls):
        return cls.counter


# Summary:
# For BFS we used Queues to complete this. We ran into minor road blocks on getting
# this to work, but eventually overcame them.
class BfsSpider(scrapy.Spider):
    name = "bfs"
    counter = 0
    limit = 10


    def __init__(self):

        file = open('global_settings.txt', 'r')

        for index, arg in enumerate(file.readlines()):
            if index == 0:
                self.urls = [arg.strip()]
            if index == 1:
                self.limit = int(arg.strip())
            if index == 2:
                self.directory = arg.strip()

        self.visited = set()
        self.queue = []

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        if self.counter >= self.limit:
            raise CloseSpider('Limit Reached')

        self.write_contents(response, self._get_counter())
        self._increase_counter()



        urls = self.collect_urls(response)  # All the urls in one page

        # Loop through the urls, write all contents of neighbors
        for url in urls:
            if url not in self.visited:
                self.visited.add(url)
                self.queue.append(url)

        for url in self.queue:
            yield scrapy.Request(url=self.queue.pop(0), callback=self.parse) # Recursively call on the url



    def write_contents(self, response, counter):
        filename = str(counter) + '.html'
        filename = os.path.join(self.directory, filename)
        with open(filename, 'w') as f:
            f.write(str(response.body))
        self.log('Saved file %s' % filename)

        with open('index.dat', 'a') as file:
            file.write(filename + ' ' + str(response.url) + '\n')

    def collect_urls(self, response):
        urls = []
        # Collect all the links in current page, append to urls
        for sel in response.xpath('//a'):
            res = sel.xpath('@href').extract()
            if not res:
                continue
            res = res[0]
            if 'http' not in res:
                res = urllib.parse.urljoin(response.url, res)
            urls.append(res)
        return urls

    @classmethod
    def _increase_counter(cls):
        cls.counter += 1

    @classmethod
    def _get_counter(cls):
        return cls.counter
