import scrapy
from ..items import GameItem


class EbaySpider(scrapy.Spider):
    name = 'ebay_spider'
    allowed_domains = ['ebay.fr']
    start_urls = [
        'https://www.ebay.fr/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=consoles+nintendo&_sacat=0&_odkw=consoles+nintendo&_osacat=0',
        'https://www.ebay.fr/sch/i.html?_from=R40&_trksid=p3711649.m570.l1313&_nkw=consoles+playstation&_sacat=0',
        'https://www.ebay.fr/sch/139971/i.html?_from=R40&_nkw=concoles+xbox',
        'https://www.ebay.fr/sch/i.html?_from=R40&_trksid=p3711649.m570.l1313&_nkw=consoles+retrogaming&_sacat=0',
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    def parse(self, response):
        self.logger.info(f"Currently scraping: {response.url}")

        # Extraction des produits
        products = response.xpath('//li[contains(@class, "s-item")]')
        if not products:
            self.logger.warning(f"No products found on: {response.url}")
        else:
            self.logger.info(f"Found {len(products)} products on: {response.url}")

        for product in products:
            item = GameItem()
            name = product.xpath('.//div[contains(@class, "s-item__title")]/span/text()').get()

            # Ignorer les résultats avec "Shop on eBay" ou des noms nuls
            if not name or "Shop on eBay" in name:
                continue

            item['name'] = name
            item['price'] = product.xpath('.//span[contains(@class, "s-item__price")]/text()').get()
            relative_url = product.xpath('.//a[contains(@class, "s-item__link")]/@href').get()
            item['url'] = response.urljoin(relative_url)
            yield item

        # Gestion de la pagination
        next_page = response.xpath('//a[contains(@class, "pagination__next")]/@href').get()
        if next_page:
            self.logger.info(f"Found next page: {next_page}")
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse
            )
