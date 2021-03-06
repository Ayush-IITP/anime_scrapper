#!/usr/bin/env python3

import sys
import scrapy
from scrapy.crawler import CrawlerProcess


class videourls(scrapy.Spider):
    url = sys.argv[1]
    name = "episodes"
    start_urls = [url, ]

    def parse(self, response):
        domain = "http://animeheaven.eu/"
        stream_href = response.css("a[href*=watch]::attr(href)").extract()
        stream_urls = [domain + i for i in stream_href]

        for url in stream_urls:
            yield scrapy.Request(url, callback=self.download_link)

    def download_link(self, response):
        download_links = []
        script_code = response.css("div script::text").extract_first()
        download_url = script_code.split("source src=")[1].split("type")[0].replace("'", "")[:-4]
        episode = download_url.split("--")[1]
        download_links.append([episode, download_url])

        print(download_links)

        with open("Episode_Download_Links.txt", "a") as epi_dl:
            epi_dl.write("Episode.{}  {} \n\n".format(episode, download_url))


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(videourls, domain="http://animeheaven.eu/")
    process.start()
