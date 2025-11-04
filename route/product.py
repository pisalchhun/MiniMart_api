from app import app, db
from flask import request, jsonify
from sqlalchemy import text
from model.product import Product

@app.get('/product/list')
def get_product():
    return get_all_product()


@app.get('/product/list/<int:product_id>')
def get_product_by_id(product_id):
    return get_all_by_id(product_id)


@app.post('/product/create')
def create_product():
    product = request.get_json()
    if not product:
        return jsonify({'message': 'No product data provided!'}), 400
    if not product.get('product_name'):
        return jsonify({'message': 'Product name is required!'}), 400
    if not product.get('qty'):
        return jsonify({'message': 'Quantity is required!'}), 400
    if not product.get('price'):
        return jsonify({'message': 'Price is required!'}), 400

    product_name = product.get('product_name')
    qty = product.get('qty')
    price = product.get('price')
    category_id = product.get('category_id')
    product_obj = Product(
        product_name=product_name,
        qty = qty,
        price = price,
        category_id = category_id
                          )
    db.session.add(product_obj)
    db.session.commit()

    return jsonify({
        'status': 'Create product success!'
    }), 201


@app.put('/product/update')
def update_product():
    product = request.get_json()
    if not product:
        return jsonify({'message': 'No product data provided!'}), 400
    if not product.get('product_id'):
        return jsonify({'message': 'Product id is required!'}), 400
    if not product.get('product_name'):
        return jsonify({'message': 'product name is required!'}), 400
    if not product.get('qty'):
        return jsonify({'message': 'Quantity is required!'}), 400
    if not product.get('price'):
        return jsonify({'message': 'Price is required!'}), 400

    product_name = product.get('product_name')
    qty = product.get('qty')
    price = product.get('price')
    category_id = product.get('category_id')
    product_obj = Product.query.get(product.get('product_id'))
    if not product_obj:
        return jsonify({'message': 'product not found!'}), 404

    product_obj.product_name = product_name
    product_obj.qty = qty
    product_obj.price = price
    product_obj.category_id = category_id

    db.session.commit()

    return jsonify({
        'status': 'Update product success!'\

    }), 200


@app.delete('/product/delete')
def product_user():
    product = request.get_json()
    if not product.get('product_id'):
        return jsonify({'message': 'product id is required!'}), 400


    product_id = product.get('product_id')

    product_obj = Product.query.get(product_id)
    if not product_obj:
        return jsonify({'message': 'product not found!'}), 404
    db.session.delete(product_obj)
    db.session.commit()
    return jsonify({
        'status': 'Delete product success!'
    }), 200

def get_all_product():
    sql = text("SELECT * FROM product")
    result = db.session.execute(sql).fetchall()

    if not result:
        return jsonify({'message': 'No products found!'}), 404

    rows = [dict(row._mapping) for row in result]
    return jsonify(rows), 200


def get_all_by_id(product_id: int):
    sql = text("SELECT * FROM product ")
    result = db.session.execute(sql, {"category_id": product_id}).fetchone()

    if not result:
        return jsonify({'error': 'Product not found!'}), 404

    row = dict(result._mapping)
    return jsonify(row), 200





