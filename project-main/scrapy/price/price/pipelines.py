from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from mysql import connector
import re
from datetime import datetime


class ProjetPipeline:
    def process_item(self, item, spider):
        return item

    @staticmethod
    def clean_price(price):
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


# Pipeline pour enregistrer les items des sites dans la base de données.
class MySQLPipeline:
    def __init__(self):
        try:
            self.connexion = connector.connect(
                host="localhost",
                user="user",
                password="passwordUser0",
                database="comparatordb0",
                port=3308
            )
            self.cursor = self.connexion.cursor()
            print("Connexion MySQL réussie")
        except Exception as e:
            print(f"Erreur de connexion MySQL : {e}")
            self.connexion = None  # Ajoutez ceci pour éviter d'autres erreurs

    @staticmethod
    def clean_price(price):
        """
        Nettoie et convertit le prix en float en supprimant les symboles € ou EUR.
        """
        if price:
            price = price.replace('€', '').replace('EUR', '').strip()
            try:
                return float(price.replace(',', '.'))
            except ValueError:
                print(f"Impossible de convertir le prix: {price}")
        return None

    def process_item(self, item, spider):
        spider.logger.info(f"Pipeline : Item reçu pour insertion : {item}")
        
        # Nettoyez le prix avant insertion
        if 'price' in item:
            item['price'] = self.clean_price(item['price'])

        query = """
        INSERT INTO articles (name, price, url)
        VALUES (%s, %s, %s)
        """
        try:
            self.cursor.execute(query, (item['name'], item['price'], item['url']))
            self.connexion.commit()
            spider.logger.info(f"Item inséré avec succès : {item}")
        except Exception as e:
            spider.logger.error(f"Erreur lors de l'insertion dans MySQL : {e}")
            self.connexion.rollback()
        return item

    def close_spider(self, spider):
        if self.cursor:
            self.cursor.close()
        if self.connexion:
            self.connexion.close()
