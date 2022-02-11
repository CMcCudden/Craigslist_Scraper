from flask import Flask, render_template
from database import Database

app = Flask(__name__)
db = Database()

# fetch all the listings from the db
db.get_all_search_listings()


@app.route('/')
def home():
    db.get_all_search_listings()
    return render_template("index.html")


@app.route('/listings/<string:city>')
def show_listing(city):
    listings = db.get_all_search_listings_by_city(city)
    # for listing in data:
    #     if listing.city == city:
    #         print(f"address: {listing.address} price: {listing.price} url {listing.url} date: {listing.date}"
    #                f"city: {listing.city}")
    return render_template("rentals.html", listings=listings)


if __name__ == "__main__":
    app.run(debug=True)
