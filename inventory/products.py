products = {

    "iphone 15": {
        "price": 1200,
        "stock": 12
    },

    "samsung s24": {
        "price": 950,
        "stock": 20
    },

    "airpods pro": {
        "price": 250,
        "stock": 50
    }
}

def search_product(query):

    query = query.lower()

    for product in products:

        if query in product:
            return products[product]

    return None