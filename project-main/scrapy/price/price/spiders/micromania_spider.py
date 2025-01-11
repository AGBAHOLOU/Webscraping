import scrapy
from ..items import GameItem


class MicromaniaSpider(scrapy.Spider):
    name = 'micromania_spider'
    allowed_domains = ['micromania.fr']
    start_urls = ['https://www.micromania.fr/consoles-ps4.html',
                  'https://www.micromania.fr/consoles-ps5.html',
                  'https://www.micromania.fr/consoles-switch.html',
                  'https://www.micromania.fr/consoles-xbox.html',
                  'https://www.micromania.fr/occasion-consoles.html',
                  'https://www.micromania.fr/toutes-les-consoles.html'
                  ]

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    def parse(self, response):
        self.logger.info(f"Currently scraping: {response.url}")

        # Extraction des produits
        products = response.xpath('//div[contains(@class, "product-tile-body")]')
        if not products:
            self.logger.warning("No products found!")
        else:
            self.logger.info(f"Found {len(products)} products on: {response.url}")

        for product in products:
            item = GameItem()

            # Nom du produit
            raw_name = product.xpath('.//div[@class="product-name"]/text()').get()
            if raw_name:
                item['name'] = raw_name.strip().replace('\n', '')

            # Prix du produit
            raw_price = product.xpath('.//span[@class="value"]/text()').get()
            if raw_price:
                item['price'] = raw_price.strip().replace('\n', '')

            # URL du produit
            relative_url = product.xpath('//a[@class="product-name-link pdp-link tile-text-transform-none"]/@href').get()
            if relative_url:
                item['url'] = response.urljoin(relative_url)
            else:
                item['url'] = None

            yield item

        # Gestion de la pagination
        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page:
            self.logger.info(f"Found next page: {next_page}")
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse
            )
