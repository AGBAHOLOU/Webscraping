import scrapy
from ..items import GameItem

class BonPlansEasyCashSpider(scrapy.Spider):
    name = 'bonplans_easycash_spider'
    allowed_domains = ['bons-plans.easycash.fr']
    start_urls = ['https://bons-plans.easycash.fr/consoles/nintendo?filterType=searchResults&limit=50',
                  'https://bons-plans.easycash.fr/consoles/sony?filterType=searchResults&limit=50',
                  'https://bons-plans.easycash.fr/consoles/microsoft?filterType=searchResults&limit=50',
                  'https://bons-plans.easycash.fr/retrogaming/consoles-retro?filterType=searchResults&limit=50']

    def parse(self,response):
        games = response.xpath('//li[@class="clearfix block-link"]')
        for game in games:
            new_item_game = GameItem()
            name_text = game.xpath('./div[@class="infos-container"]/div/div/h2/a/text()').get()
            cleaned_name = name_text.replace("Jeux Vidéo","").strip() if name_text else None

            if "Game Gear" in cleaned_name:
                cleaned_name = cleaned_name.replace("Game Gear","")
            if "Lynx" or "Atari 2600" or "atari 2600" in cleaned_name:
                cleaned_name = cleaned_name.replace("Atari 2600","").replace("Lynx","").replace("atari 2600","")
            if "Saturn" in cleaned_name:
                cleaned_name = cleaned_name.replace("Saturn","")
            if "Master System" in cleaned_name:
                cleaned_name = cleaned_name.replace("Master System", "")
            if "Megadrive" in cleaned_name:
                cleaned_name = cleaned_name.replace("Megadrive","")
            if "Dreamcast" in cleaned_name:
                cleaned_name = cleaned_name.replace("Dreamcast","")
            if "NES/Famicom" in cleaned_name:
                cleaned_name = cleaned_name.replace("NES/Famicom","")
            if "Super Nintendo" in cleaned_name:
                cleaned_name = cleaned_name.replace("Super Nintendo","")
            if "Nintendo 64" in cleaned_name:
                cleaned_name = cleaned_name.replace("Nintendo 64","")
            if "Game Cube" in cleaned_name:
                cleaned_name = cleaned_name.replace("Game Cube","")

            new_item_game['name'] = cleaned_name
            
            price = game.xpath('.//span[@class="infos-price-number"]/text()').get()
            price_euro = f"{price}€" if price else None
            new_item_game['price'] = price_euro
            new_item_game['url'] = game.xpath('./@data-href').get()

            yield new_item_game

        next = response.xpath('//li[@class="next"]/a/@href').get()
        if next is not None:
            next = response.urljoin(next)
            i = 0
            print("Page n°", i+1 , next)
            yield scrapy.Request(url=next, callback=self.parse)