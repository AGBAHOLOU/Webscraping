# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProjetItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field() and
    pass

class GameItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    site = scrapy.Field()