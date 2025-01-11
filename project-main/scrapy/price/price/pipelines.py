# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from mysql import connector
import re
from datetime import datetime
 
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
    


# Pipeline pour enregistrer les items des sites dans la base de données.
class MySQLPipeline:
    def __init__(self):
        self.connexion = connector.connect(
            host="mysql",
            user="user",
            password="passwordUser0",
            database="comparatordb0"
        )
        self.cursor = self.connexion.cursor()
 
    def process_item(self, item, spider):
        # Vérification ou insertion dans la table "game"
        game_result = self.select_one("game", "idgame", {"game_name": item['name']})
 
        if game_result is None:
            self.insert("game", {"game_name": item['name']})
            game_result = self.select_one("game", "idgame", {"game_name": item['name']})
 
        # Exemple de gestion avec un site par défaut
        website_result = self.select_one("website", "idwebsite", {"website_name": "default_site"})
        if website_result is None:
            self.insert("website", {"website_name": "default_site"})
            website_result = self.select_one("website", "idwebsite", {"website_name": "default_site"})
 
        # Vérification ou insertion dans la table "price"
        price_result = self.select_one("price", "idprice", {
            "price_idgame": game_result[0],
            "price_idwebsite": website_result[0]
        })
 
        if price_result is None:
            self.insert("price", {
                "price_idgame": game_result[0],
                "price_idwebsite": website_result[0],
                "price_value": item["price"],
                "price_insertdate": datetime.now(),
                "price_url": item['url']
            })
        else:
            self.update("price", {
                "price_value": item["price"],
                "price_updatedate": datetime.now()
            }, {
                "price_idgame": game_result[0],
                "price_idwebsite": website_result[0]
            })
 
        return item
 
    def insert(self, table, values):
        placeholders = ', '.join(['%s'] * len(values))
        query = "INSERT INTO {} ({}) VALUES ({})".format(table, ', '.join(values.keys()), placeholders)
        self.cursor.execute(query, list(values.values()))
        self.connexion.commit()
 
    def update(self, table, set_values, where):
        set_clause = ', '.join(['{} = %s'.format(col) for col in set_values])
        where_clause = ' AND '.join(['{} = %s'.format(col) for col in where])
        query = "UPDATE {} SET {} WHERE {}".format(table, set_clause, where_clause)
        self.cursor.execute(query, list(set_values.values()) + list(where.values()))
        self.connexion.commit()
 
    def select_one(self, table, columns="*", where=None):
        query = "SELECT {} FROM {}".format(columns, table)
        if where is not None:
            query += " WHERE {}".format(" AND ".join(['{} = %s'.format(col) for col in where]))
        self.cursor.execute(query, list(where.values()) if where else None)
        return self.cursor.fetchone()

