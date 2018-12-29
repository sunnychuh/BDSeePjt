# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BdseepjtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    link = scrapy.Field()
    comments_num = scrapy.Field()
    published_date = scrapy.Field()
    category = scrapy.Field()
    category_tag = scrapy.Field()
    image_url = scrapy.Field()
    score = scrapy.Field()

class BdseepjtItemDetail(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    descriptions = scrapy.Field()
    contents = scrapy.Field()
    content_imgs = scrapy.Field()
    download_links = scrapy.Field()
    comments_num = scrapy.Field()
    published_date = scrapy.Field()
    category = scrapy.Field()
    category_tag = scrapy.Field()
    image_url = scrapy.Field()
    score = scrapy.Field()