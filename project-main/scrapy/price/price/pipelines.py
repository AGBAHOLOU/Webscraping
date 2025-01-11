# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
 
class ProjetPipeline:
    def process_item(self, item, spider):
        return item
 
    def clean_price(self, price):
        """
        Nettoie et convertit le prix en float en supprimant les symboles € ou EUR.
        """
        if price:
            price = price.replace('€', '').replace('EUR', '').strip()
            try:
                return float(price.replace(',', '.'))
            except ValueError:
                spider.logger.warning(f"Impossible de convertir le prix: {price}")
        return None
   
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'price' in adapter:
            adapter['price'] = self.clean_price(adapter['price'])
        return item
    


    