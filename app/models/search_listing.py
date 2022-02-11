class SearchListing:
    def __init__(self, address, price, url, date, city, picture, id=None):
        self.id = id
        self.address = address
        self.price = price
        self.url = url
        self.date= date
        self.city = city
        self.picture = picture
