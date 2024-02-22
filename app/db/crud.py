from app.db.create_db import session, Product
from datetime import datetime
def create_product(name: str, price: float, expiry: str):
    '''
    Create a new product
    '''
    # Create new product
    new_product = Product(name=name, price=price, expiry=expiry)
    # Add new product to session
    session.add(new_product)
    # Commit session
    session.commit()
    return new_product

def get_all_products():
    '''
    Get all products
    '''
    return session.query(Product).all()

def del_product(id: int):
    '''
    Delete a product by id
    '''
    # Get product by id
    product = session.query(Product).get(id)
    # Delete product
    session.delete(product)
    # Commit session
    session.commit()

def edit_product(id: int, name: str, price: float, expiry: str):
    '''
    Edit a product by id
    '''
    # Get product by id
    product = session.query(Product).get(id)
    # Edit product
    product.name = name
    product.price = price
    product.expiry = expiry
    # Commit session
    session.commit()