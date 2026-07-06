products = {

    "iphone 15": {"price": 1200,"stock": 12},
    
    "samsung s24": {"price": 950,"stock": 20},
    
    "airpods pro": {"price": 250,"stock": 50},
    
    "MacBook Pro": {"price": 2000,"stock": 5},
    
    "google pixel 8": {"price": 800,"stock": 15},
    
    "sony wh-1000xm5": {"price": 350,"stock": 30},
    
    "lenovo thinkpad x1": {"price": 1800,"stock": 8},
    
    "Ipad Pro": {"price": 1100,"stock": 10},
    
    "nintendo switch": {"price": 400,"stock": 25},
    
    "nikon z9": {"price": 5500,"stock": 3},
    
    "bose quietcomfort 45": {"price": 330,"stock": 40},
    
    "dji mavic 3": {"price": 2200,"stock": 7},
    
    "canon eos r5": {"price": 3900,"stock": 4},
    
    "quick charge power bank": {"price": 60,"stock": 100},
    
    "anker soundcore liberty air 2": {"price": 80,"stock": 60},
    
    "fitbit charge 5": {"price": 150,"stock": 35},
    
    "samsung galaxy watch 5": {"price": 300,"stock": 20},
    
    "sony a7 iv": {"price": 2500,"stock": 6},
    
    "jbl flip 6": {"price": 120,"stock": 45},
    
    "amazon echo dot (5th gen)": {"price": 50,"stock": 80},
    
    "logitech mx master 3": {"price": 100,"stock": 25},
    
    "bose soundlink mini": {"price": 100,"stock": 30},
    
    "anker powerline ii lightning cable": {"price": 20,"stock": 150},
    
    "samsung t7 portable ssd": {"price": 150,"stock": 20},
    
    "apple watch series 7": {"price": 400,"stock": 15},
    
    "sony playstation 5": {"price": 500,"stock": 10},
    
    "xbox series x": {"price": 500,"stock": 10},
    
    "nintendo switch oled": {"price": 350,"stock": 20},
    
    "google nest hub (2nd gen)": {"price": 100,"stock": 30},
    
    "anker powercore 10000": {"price": 30,"stock": 100},
    
    "samsung galaxy buds pro": {"price": 200,"stock": 25},
    
    "apple airpods max": {"price": 550,"stock": 10},
    
    "logitech g pro x super matic": {"price": 150,"stock": 20},
    
    "Logitech Mouse": {"price": 0,"stock": 0},
    
    "Logitech Keyboard": {"price": 0,"stock": 0},
    
    "Logitech Headset": {"price": 0,"stock": 0},
    
    "Logitech Webcam": {"price": 0,"stock": 0},
    
    "Logitech Speaker": {"price": 0,"stock": 0},
    
    "Logitech Mousepad": {"price": 0,"stock": 0},
    
    "Logitech Wireless Mouse": {"price": 0,"stock": 0},
    
    "Logitech Wireless Keyboard": {"price": 0,"stock": 0},
    
    "Logitech Wireless Headset": {"price": 0,"stock": 0},
    
    "Logitech Wireless Webcam": {"price": 500,"stock": 10}, 
    
    "sony xperia 1 iii": {"price": 1200,"stock": 12},
    
    "samsung galaxy s24": {"price": 950,"stock": 20},
    
}

def search_product(query):

    query = query.lower()

    for product in products:

        if query in product:
            return products[product]

    return None