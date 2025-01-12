import scrapy
from ..items import GameItem

def uniformize_name_and_category(name):
    """Uniformise le nom des consoles et attribue la catégorie correspondante."""
    name = name.lower()
    categories = []
    uniform_name = None

    # Sony
    if any(term in name for term in ["ps5", "playstation 5", "playstation5"]):
        uniform_name = "PlayStation 5"
        categories.append("Sony")
    elif any(term in name for term in ["ps4", "playstation 4", "playstation4"]):
        uniform_name = "PlayStation 4"
        categories.append("Sony")
    elif any(term in name for term in ["ps3", "playstation 3", "playstation3"]):
        uniform_name = "PlayStation 3"
        categories.append("Sony")
    elif any(term in name for term in ["ps2", "playstation 2", "playstation2"]):
        uniform_name = "PlayStation 2"
        categories.append("Sony")
    elif any(term in name for term in ["ps1", "playstation 1", "playstation classic", "ps one"]):
        uniform_name = "PlayStation 1"
        categories.append("Sony")

    # Microsoft
    elif any(term in name for term in ["xbox series x", "xbox series s", "xbox series"]):
        uniform_name = "Xbox Series X/S"
        categories.append("Microsoft")
    elif "xbox one" in name:
        uniform_name = "Xbox One"
        categories.append("Microsoft")
    elif "xbox 360" in name:
        uniform_name = "Xbox 360"
        categories.append("Microsoft")

    # Nintendo
    elif any(term in name for term in ["switch", "nintendo switch", "switch lite", "switch oled"]):
        uniform_name = "Nintendo Switch"
        categories.append("Nintendo")
    elif any(term in name for term in ["wii", "nintendo wii", "wii u", "wii mini"]):
        uniform_name = "Nintendo Wii"
        categories.append("Nintendo")
    elif any(term in name for term in ["gamecube", "nintendo gamecube"]):
        uniform_name = "Nintendo GameCube"
        categories.append("Nintendo")
    elif any(term in name for term in ["nintendo 64", "n64"]):
        uniform_name = "Nintendo 64"
        categories.append("Nintendo")
    elif any(term in name for term in ["nes", "nintendo nes", "classic mini nes"]):
        uniform_name = "Nintendo NES"
        categories.append("Nintendo")

    # Retrogaming
    elif any(term in name for term in ["sega", "megadrive", "master system", "dreamcast", "saturn"]):
        uniform_name = "Sega Consoles"
        categories.append("Retrogaming")
    elif any(term in name for term in ["atari", "atari flashback", "atari 2600"]):
        uniform_name = "Atari Consoles"
        categories.append("Retrogaming")
    elif any(term in name for term in ["neo-geo", "snk neo-geo"]):
        uniform_name = "Neo-Geo"
        categories.append("Retrogaming")

    return uniform_name, categories


class MicromaniaSpider(scrapy.Spider):
    name = 'micromania_spider'
    allowed_domains = ['micromania.fr']
    start_urls = [
        'https://www.micromania.fr/consoles-ps4.html',
        'https://www.micromania.fr/consoles-ps5.html',
        'https://www.micromania.fr/consoles-switch.html',
        'https://www.micromania.fr/consoles-xbox.html',
        'https://www.micromania.fr/occasion-consoles.html'
    ]

    def parse(self, response):
        products = response.xpath('//div[contains(@class, "product-tile-body")]')
        for product in products:
            item = GameItem()

            # Récupération de l'image
            image_url = product.xpath('//picture/source[@media="(min-width: 768px)"]/@data-srcset').get()
            item['image'] = image_url

            # Extraction du nom
            raw_name = product.xpath('.//div[@class="product-name"]/text()').get()
            if raw_name:
                uniform_name, categories = uniformize_name_and_category(raw_name)
                if not uniform_name:  # Si le nom uniformisé est null, ignorer cet article
                    continue
                item['name'] = uniform_name
                item['category'] = categories
            else:
                continue  # Si aucun nom brut, ignorer l'article

            # Extraction du prix
            raw_price = product.xpath('.//span[@class="value"]/text()').get()
            if not raw_price:  # Si le prix est nul, ignorer cet article
                continue
            item['price'] = raw_price.strip().replace('\n', '')

            # URL du produit
            relative_url = product.xpath('//a[@class="product-name-link pdp-link tile-text-transform-none"]/@href').get()
            item['url'] = response.urljoin(relative_url) if relative_url else None

            # Nom du site
            item['site'] = self.allowed_domains[0]

            yield item

        # Gestion de la pagination
        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
