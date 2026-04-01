import uuid
import random

# Simulated product database from multiple platforms
MOCK_PRODUCTS = [
    {"name": "Dell XPS 13", "brand": "Dell", "category": "Laptop"},
    {"name": "Apple MacBook Pro 14", "brand": "Apple", "category": "Laptop"},
    {"name": "Apple MacBook Air M2", "brand": "Apple", "category": "Laptop"},
    {"name": "Samsung Galaxy S23 Ultra", "brand": "Samsung", "category": "Smartphone"},
    {"name": "Apple iPhone 15 Pro", "brand": "Apple", "category": "Smartphone"},
    {"name": "Google Pixel 8 Pro", "brand": "Google", "category": "Smartphone"},
    {"name": "OnePlus 12", "brand": "OnePlus", "category": "Smartphone"},
    {"name": "Sony WH-1000XM5", "brand": "Sony", "category": "Headphones"},
    {"name": "Bose QuietComfort 45", "brand": "Bose", "category": "Headphones"},
    {"name": "Nintendo Switch OLED", "brand": "Nintendo", "category": "Gaming"},
    {"name": "Sony PlayStation 5", "brand": "Sony", "category": "Gaming"},
    {"name": "Logitech MX Master 3S", "brand": "Logitech", "category": "Accessories"}
]

PLATFORMS = ["Amazon", "BestBuy", "Walmart"]

def generate_mock_variants(product):
    """Generates price variants and discounts for a single product across different platforms."""
    variants = []
    base_price = random.randint(300, 1200) + 0.99
    
    for platform in PLATFORMS:
        original_price = base_price * random.uniform(1.05, 1.35)
        price_offset = random.uniform(-0.15, 0.05) * base_price
        final_price = round(base_price + price_offset, 2)
        
        if final_price >= original_price:
            original_price = final_price * 1.15
            
        original_price = round(original_price, 2)
        discount_amount = original_price - final_price
        discount_percentage = int(round((discount_amount / original_price) * 100))
        
        # Ensure at least 5% discount for effect
        if discount_percentage < 5:
            discount_percentage = random.randint(5, 15)
            original_price = round(final_price / (1 - (discount_percentage/100.0)), 2)

        variants.append({
            "id": str(uuid.uuid4()),
            "platform": platform,
            "product_name": product["name"],
            "original_price": original_price,
            "price": final_price,
            "discount_percentage": discount_percentage,
            "url": f"https://mocked.{platform.lower()}.com/{product['name'].replace(' ', '-').lower()}",
            "in_stock": random.choice([True, True, True, False]),
            "image": f"https://via.placeholder.com/150/ffffff/333333?text={product['name'].replace(' ', '+')}"
        })
    return variants

def search_products(query: str):
    """
    Service method to search for products and return compared deals with discounts highlighted.
    """
    if not query:
        return []
        
    query = query.lower()
    results = []
    
    # We display all if query is 'smartphone' or 'smartphones' and it matches the category
    search_term = 'smartphone' if query == 'smartphones' else query
    
    for product in MOCK_PRODUCTS:
        # Match by name, brand, or category
        if search_term in product["name"].lower() or search_term in product["brand"].lower() or search_term in product["category"].lower():
            variants = generate_mock_variants(product)
            
            in_stock_variants = [v for v in variants if v["in_stock"]]
            if in_stock_variants:
                lowest_price_variant = min(in_stock_variants, key=lambda x: x["price"])
                lowest_price_id = lowest_price_variant["id"]
                
                biggest_discount_variant = max(in_stock_variants, key=lambda x: x["discount_percentage"])
                biggest_discount_id = biggest_discount_variant["id"]
            else:
                lowest_price_id = None
                biggest_discount_id = None
                
            for variant in variants:
                variant["is_lowest"] = (variant["id"] == lowest_price_id)
                variant["is_biggest_discount"] = (variant["id"] == biggest_discount_id)
                
            variants.sort(key=lambda x: x["price"])
            
            results.append({
                "product": product,
                "deals": variants
            })
            
    return results
