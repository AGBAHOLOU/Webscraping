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

    return uniform_name, ", ".join(categories)  # Convertir les catégories en chaîne de caractères


class BonPlansEasyCashSpider(scrapy.Spider):
    name = 'bonplans_easycash_spider'
    allowed_domains = ['bons-plans.easycash.fr']
    start_urls = [
        'https://bons-plans.easycash.fr/consoles/nintendo?filterType=searchResults&limit=50',
        'https://bons-plans.easycash.fr/consoles/sony?filterType=searchResults&limit=50',
        'https://bons-plans.easycash.fr/consoles/microsoft?filterType=searchResults&limit=50',
        'https://bons-plans.easycash.fr/retrogaming/consoles-retro?filterType=searchResults&limit=50'
    ]

    def parse(self, response):
        games = response.xpath('//li[@class="clearfix block-link"]')
        for game in games:
            new_item_game = GameItem()

            # Récupération de l'image
            image_url = game.xpath('//div[@class="image"]//img/@src').get()
            new_item_game['image'] = image_url

            # Extraction du nom
            name_text = game.xpath('./div[@class="infos-container"]/div/div/h2/a/text()').get()
            if name_text:
                uniform_name, categories = uniformize_name_and_category(name_text)
                if not uniform_name:  # Si le nom uniformisé est null, ignorer cet article
                    continue
                new_item_game['name'] = uniform_name
                new_item_game['category'] = categories  # Enregistrer comme chaîne de caractères
            else:
                continue  # Si aucun nom brut, ignorer l'article

            # Récupération du prix
            price = game.xpath('.//span[@class="infos-price-number"]/text()').get()
            new_item_game['price'] = f"{price}€" if price else None

            # Récupération de l'URL du produit
            new_item_game['url'] = game.xpath('./@data-href').get()

            # Ajout du nom du site
            new_item_game['site'] = self.allowed_domains[0]

            yield new_item_game

        # Gestion de la pagination
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
