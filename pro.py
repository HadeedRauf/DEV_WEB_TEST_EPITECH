from main import db
from model import Product, Category
from datetime import date

products_to_add = [
    {
        'product_name': 'Apple',
        'price': 0.5,
        'quantity': 100,
        'manufacturing_date': date(2026, 1, 1),
        'expiring_date': date(2026, 6, 1),
        'unit': 'kg',
        'category_name': 'Fruits'
    },
    {
        'product_name': 'Milk',
        'price': 1.2,
        'quantity': 50,
        'manufacturing_date': date(2026, 2, 1),
        'expiring_date': date(2026, 2, 20),
        'unit': 'liter',
        'category_name': 'Dairy'
    },
    {
        'product_name': 'Bread',
        'price': 1.0,
        'quantity': 80,
        'manufacturing_date': date(2026, 2, 15),
        'expiring_date': date(2026, 2, 22),
        'unit': 'loaf',
        'category_name': 'Bakery'
    }
]

def get_or_create_category(name):
    category = Category.query.filter_by(category_name=name).first()
    if not category:
        category = Category(category_name=name)
        db.session.add(category)
        db.session.commit()
    return category

def add_products():
    from main import app
    with app.app_context():
        for prod in products_to_add:
            category = get_or_create_category(prod['category_name'])
            # Prevent duplicate products (by name and category)
            existing = Product.query.filter_by(product_name=prod['product_name'], category_id=category.category_id).first()
            if existing:
                print(f"Product '{prod['product_name']}' already exists in category '{category.category_name}'. Skipping.")
                continue
            product = Product(
                product_name=prod['product_name'],
                price=prod['price'],
                quantity=prod['quantity'],
                manufacturing_date=prod['manufacturing_date'],
                expiring_date=prod['expiring_date'],
                product_image=prod.get('product_image', None),
                unit=prod['unit'],
                category_id=category.category_id
            )
            db.session.add(product)
        db.session.commit()
        print('Products added successfully!')

if __name__ == '__main__':
    add_products()
