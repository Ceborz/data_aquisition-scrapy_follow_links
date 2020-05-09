# -*- coding: utf-8 -*-
import scrapy
from scrapy_follow_links.items import articles
from scrapy.http.request import Request


class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['http://en.wikipedia.org/wiki/Wikipedia:Featured_articles']

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'file:C://Users//rzepeda//Documents//masters//applied_data_science//03_data_acquisiton_and_preparation//homeworks//data_aquisition-scrapy_follow_links//featured_article-%(time)s.json'
    }

    def parse(self, response):

        host = self.allowed_domains[0]

        for link in response.css(".featured_article_metadata > a"):
            url = f"https://{host}{link.attrib.get('href')}"
            yield response.follow(
                url,
                callback = self.parse_link,
                meta = {
                    'link': url
                }
            )

    def parse_link(self, response):
        p_text = ''
        for p in response.css("#mw-content-text > .mw-parser-output > p"):
            texts = p.css('*::text')
            has_text = False
            for text_in_p in texts:
                if text_in_p and text_in_p.get() and not text_in_p.get().isspace():
                    p_text += text_in_p.get()
                    has_text = True
            
            if has_text:
                break

        return articles (
            link = response.meta['link'],
            body = {
                'title': response.css('#firstHeading::text').get(),
                'paragraph': p_text
            }
        )
