import os
import logging
import sys
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
from typing import List
from models.search_listing import SearchListing

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class Database:
    def __init__(self) -> None:
        load_dotenv()
        self.conn = psycopg2.connect(
            dbname=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT")
        )
        self.conn.set_session(autocommit=True)
        self.cur = self.conn.cursor()
        logging.info('Successfully connected to db')

    def close(self) -> None:
        self.cur.close()
        self.conn.close()

    def debug_query(self) -> None:
        """Logs SQL command queued on cursor"""

        query = self.cur.query.decode("utf-8")
        logging.debug(f"Executed query: {query}")

    def create_city_state_table(self) -> None:
        logging.debug(f"Attempting to create city_state table.")
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS city_state (
                id serial PRIMARY KEY,
                city VARCHAR(25),
                state VARCHAR(25)
            );
            """
        )
        self.debug_query()

    def insert_city(self) -> int:
        logging.debug(
            f"Attempting to insert cities.")
        self.cur.execute(
            """
            INSERT INTO city_state (city, state)
            VALUES ('New York', 'NY'),
            ('Los Angeles', 'CA'),
            ('Los Vegas', 'NV'),
            ('Philadelphia', 'PA'),
            ('Chicago', 'IL')
            RETURNING id;
            """,
        )
        self.debug_query()
        result = self.cur.fetchone()
        logging.debug(
            f"Successfully saved listing with id: {result[0]}")
        return int(result[0])

    def create_search_listing_table(self) -> None:
        logging.debug(f"Attempting to create table")
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS rentals (
                id serial PRIMARY KEY,
                address VARCHAR(200),
                price INTEGER,
                url VARCHAR(200),
                date TIMESTAMP,
                city VARCHAR(25)
            );
            """
        )
        self.debug_query()

    def insert_search_listing(self, search_listing) -> int:
        logging.debug(
            f"Attempting to insert rentals: {search_listing}")
        self.cur.execute(
            """
            INSERT INTO rentals (address, price, url, date, city, picture)
            VALUES (%(addr)s, %(price)s, %(url)s, %(date)s, %(city)s, %(picture)s)
            RETURNING id;
            """,
            {
                "addr": search_listing.address,
                "price": search_listing.price,
                "url": search_listing.url,
                "date": search_listing.date,
                "city": search_listing.city,
                "picture": search_listing.picture
            }
        )
        self.debug_query()
        result = self.cur.fetchone()
        logging.debug(
            f"Successfully saved listing with id: {result[0]}")
        return int(result[0])

    def get_all_search_listings(self) -> List:
        logging.debug(
            f"Attempting to return all search listings")
        self.cur.execute(
            """
            SELECT * FROM rentals;
            """
        )
        self.debug_query()
        results = []
        for record in self.cur.fetchall():
            results.append(
                SearchListing(id=record[0], address=record[1], price=record[2], url=record[3], date=record[4], city=record[5],
                              picture=record[6]))

        logging.debug(f"Successfully fetched all {len(results)} records")
        return results

    def get_all_search_listings_by_city(self, city) -> List:
        logging.debug(
            f"Attempting to return all search listings for {city}")
        self.cur.execute(
            f"""
            SELECT * FROM rentals WHERE city='{city}';
            """
        )
        self.debug_query()
        results = []
        for record in self.cur.fetchall():
            results.append(
                SearchListing(id=record[0], address=record[1], price=record[2], url=record[3], date=record[4], city=record[5],
                              picture=record[6]))

        logging.debug(f"Successfully fetched all {len(results)} records")
        return results

    def delete_search_listing_emptystr(self,) -> None:
        logging.info(
            f"Attempting to delete listings with no addresses.")
        self.cur.execute(
            f"""
            DELETE FROM rentals WHERE address = '( )';
            """
        )
        self.debug_query()
        result = self.cur.fetchone()
        logging.debug(
            f"Successfully deleted listing with id: {result[0]}")
        return result[0]

    def get_all_listings_with_price_between(self, start_range: int, end_range: int):
        logging.info(
            f"Attempting to pull requested price range of {start_range} to {end_range}"
        )
        self.cur.execute(
            f"""
                SELECT * FROM rentals WHERE price BETWEEN {start_range} AND {end_range};
            """
        )
        self.debug_query()
        results = []
        for record in self.cur.fetchall():
            results.append(
                SearchListing(id=record[0], address=record[1], price=record[2], url=record[3], date=record[4], city=record[5],
                              picture=record[6]))

    def delete_yesterdays_scrape(self) -> None:
        logging.info(
            f"Attempting to delete all listings that were scraped yesterday."
        )
        now = datetime.now()
        dt_string = now.strftime('%Y-%m-%d')
        timestamp = dt_string + ' 00:00:00'
        self.cur.execute(
            f"""
                DELETE * FROM rentals WHERE date >= timestamp '{timestamp}';
            """
        )
        self.debug_query()
        result = self.cur.fetchone()
        return result