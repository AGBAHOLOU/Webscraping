import scrapy
from ..items import GameItem

def uniformize_name_and_category(name):
    """Uniformise le nom des consoles et attribue la catégorie correspondante."""
    name = name.lower()
    categories = []
    uniform_name = None

    # Sony - PlayStation
    if any(term in name for term in [
        "ps5", "playstation 5", "playstation5", "playstation 5 slim", "ps5 slim",
        "playstation 5 digital edition", "ps5 digital edition", "playstation 5 pro", "ps5 pro",
        "ps5 standard", "playstation 5 (modèle slim)", "playstation 5 - reconditionné", "playstation 5 - occasion"
    ]):
        uniform_name = "PlayStation 5"
        categories.append("Sony")
    elif any(term in name for term in [
        "ps4", "playstation 4", "playstation4", "ps4 slim", "playstation 4 slim",
        "ps4 pro", "playstation 4 pro", "ps4 slim noire", "ps4 slim blanche", "ps4 pro noire", "ps4 pro blanche"
    ]):
        uniform_name = "PlayStation 4"
        categories.append("Sony")
    elif any(term in name for term in [
        "ps3", "playstation 3", "playstation3", "ps3 slim", "playstation 3 slim", "ps3 ultra slim"
    ]):
        uniform_name = "PlayStation 3"
        categories.append("Sony")
    elif any(term in name for term in ["ps1", "playstation 1", "playstation classic", "ps one"]):
        uniform_name = "PlayStation 1"
        categories.append("Sony")

    # Microsoft - Xbox
    elif any(term in name for term in [
        "xbox series x", "xbox series s", "xbox series", "xbox series x digital edition", "xbox series s digital edition"
    ]):
        uniform_name = "Xbox Series X/S"
        categories.append("Microsoft")
    elif any(term in name for term in ["xbox one", "xbox one s", "xbox one x"]):
        uniform_name = "Xbox One"
        categories.append("Microsoft")
    elif "xbox 360" in name:
        uniform_name = "Xbox 360"
        categories.append("Microsoft")

    # Nintendo
    elif any(term in name for term in [
        "switch", "nintendo switch", "switch lite", "switch oled", "switch animal crossing edition"
    ]):
        uniform_name = "Nintendo Switch"
        categories.append("Nintendo")
    elif any(term in name for term in ["wii", "nintendo wii", "wii u", "wii mini"]):
        uniform_name = "Nintendo Wii"
        categories.append("Nintendo")
    elif "gamecube" in name:
        uniform_name = "Nintendo GameCube"
        categories.append("Nintendo")
    elif any(term in name for term in ["nintendo 64", "n64"]):
        uniform_name = "Nintendo 64"
        categories.append("Nintendo")
    elif any(term in name for term in ["nes", "nintendo nes"]):
        uniform_name = "Nintendo NES"
        categories.append("Nintendo")

    # Retrogaming
    elif any(term in name for term in [
        "sega", "megadrive", "master system", "dreamcast", "saturn"
    ]):
        uniform_name = "Sega Consoles"
        categories.append("Retrogaming")
    elif any(term in name for term in ["atari", "atari flashback", "atari 2600"]):
        uniform_name = "Atari Consoles"
        categories.append("Retrogaming")
    elif any(term in name for term in ["neo-geo", "snk neo-geo"]):
        uniform_name = "Neo-Geo"
        categories.append("Retrogaming")

    return uniform_name, categories

class EbaySpider(scrapy.Spider):
    name = 'ebay_spider'
    allowed_domains = ['ebay.fr']
    start_urls = [
        'https://www.ebay.fr/sch/i.html?_nkw=consoles+nintendo',
        'https://www.ebay.fr/sch/i.html?_nkw=consoles+playstation',
        'https://www.ebay.fr/sch/i.html?_nkw=consoles+xbox',
        'https://www.ebay.fr/sch/i.html?_nkw=consoles+retrogaming'
    ]

    def parse(self, response):
        products = response.xpath('//li[contains(@class, "s-item")]')
        for product in products:
            item = GameItem()

            # Récupération de l'image
            image_url = product.xpath('.//div[contains(@class, "s-item__image-wrapper")]//img/@src').get()
            item['image'] = image_url

            # Extraction du nom
            raw_name = product.xpath('.//div[contains(@class, "s-item__title")]/span/text()').get()
            if raw_name:
                uniform_name, categories = uniformize_name_and_category(raw_name)
                if not uniform_name:  # Si le nom uniformisé est null, ignorer cet article
                    continue
                item['name'] = uniform_name
                item['category'] = categories
            else:
                continue  # Si aucun nom brut, ignorer l'article

            # Extraction du prix
            raw_price = product.xpath('.//span[contains(@class, "s-item__price")]/text()').get()
            if not raw_price:  # Si le prix est nul, ignorer cet article
                continue
            item['price'] = raw_price.replace(' EUR', '').replace(',', '.').strip()

            # URL du produit
            product_url = product.xpath('.//a[contains(@class, "s-item__link")]/@href').get()
            item['url'] = product_url

            # Nom du site
            item['site'] = self.allowed_domains[0]

            yield item

        # Gestion de la pagination
        next_page = response.xpath('//a[contains(@class, "pagination__next")]/@href').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
