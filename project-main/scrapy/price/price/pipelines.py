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
class MysqlPipeline:
    def __init__(self):
        self.connexion = connector.connect(
            host="mysql",
            user="user",
            password="passwordUser0",
            database="comparatordb0"
        )
        self.cursor = self.connexion.cursor()

    def process_item(self, item, spider):

        # Get the Website ID
        website_result = self.select_one("website", "idwebsite", {"website_name": item['site']})

        # If Website ID doesn't exit => insert
        if website_result is None:
            self.insert("website", {"website_name": item['site']})
            website_result = self.select_one("website", "idwebsite", {"website_name": item['site']})

        # Get the Game ID
        game_result = self.select_one("game", "idgame", {"game_name": item['nom']}) 

        # If Game ID doesn't exist => insert
        if game_result is None:
            self.insert("game", {"game_name": item['nom'], "game_type": item["type"]})
            game_result = self.select_one("game", "idgame", {"game_name": item['nom']})

        # Get the price for the key(Game ID, Website ID)
        price_result = self.select_one("price", "idprice", {"price_idgame": game_result[0], "price_idwebsite": website_result[0]})
        
        # If doesn't exist => insert
        if price_result is None:
            self.insert("price", {"price_idgame": game_result[0], "price_idwebsite": website_result[0], "price_value": item["prix"], 
            "price_insertdate": datetime.now(), "price_url": item['url']})
        # Else => Update
        elif price_result[0] != item["prix"]:
            self.update("price", {"price_value": item["prix"], "price_updatedate": datetime.now()}, 
            {"price_idgame": game_result[0], "price_idwebsite": website_result[0]})

        return item 

    def insert(self, table, values):
        # Create the placeholders string
        placeholders = ', '.join(['%s'] * len(values))
        
        # Create the INSERT query
        query = "INSERT INTO {} ({}) VALUES ({})".format(table, ', '.join(values.keys()), placeholders)

        # Execute the prepared statement
        self.cursor.execute(query, list(values.values()))
        
        # Commit the transaction
        self.connexion.commit()
    
    def update(self, table, set, where):
        # Create the SET clause
        set_clause = ', '.join(['{} = %s'.format(col) for col in set])

        # Create the UPDATE query
        query = "UPDATE {} SET {} WHERE {}".format(table, set_clause, " AND ".join(['{} = %s'.format(col) for col in where]))
        
        # Execute the prepared statement
        self.cursor.execute(query, list(set.values()) + list(where.values()))

        # Commit the transaction
        self.connexion.commit()

    def select_one(self, table, columns="*", where=None):
        # Create the SELECT query
        query = "SELECT {} FROM {}".format(columns, table)
    
        # Add the WHERE part
        if where is not None:
            query += " WHERE {}".format(" AND ".join(['{} = %s'.format(col) for col in where]))

        # Execute the prepared statement
        self.cursor.execute(query, list(where.values()))
        
        # Return the value
        return self.cursor.fetchone()