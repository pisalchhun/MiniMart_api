from app import app, db
from flask import request, jsonify
from sqlalchemy import text

from model.category import Category

@app.get('/category/list')
def get_category():
    return get_all_category()


@app.get('/category/list/<int:category_id>')
def get_category_by_id(category_id):
    return get_all_by_id(category_id)


@app.post('/category/create')
def create_category():
    category = request.get_json()
    if not category:
        return jsonify({'message': 'No category data provided!'}), 400
    if not category.get('category_name'):
        return jsonify({'message': 'Category name is required!'}), 400

    category_name = category.get('category_name')
    category_obj = Category(category_name=category_name)
    db.session.add(category_obj)
    db.session.commit()

    return jsonify({
        'status': 'Create category success!'
    }), 201


@app.put('/category/update')
def update_category():
    category = request.get_json()
    if not category:
        return jsonify({'message': 'No category data provided!'}), 400
    if not category.get('category_id'):
        return jsonify({'message': 'category id is required!'}), 400
    if not category.get('category_name'):
        return jsonify({'message': 'category name is required!'}), 400

    category_id = category.get('category_id')
    category_name = category.get('category_name')

    category_obj = Category.query.get(category_id)
    if not category_obj:
        return jsonify({'message': 'Category not found!'}), 404

    category_obj.category_name = category_name
    db.session.commit()

    return jsonify({
        'status': 'Update category success!'
    }), 200


@app.delete('/category/delete')
def category_user():
    category = request.get_json()
    if not category.get('category_id'):
        return jsonify({'message': 'category id is required!'}), 400


    category_id = category.get('category_id')
    category_name = category.get('category_name')

    category_obj = Category.query.get(category_id)
    if not category_obj:
        return jsonify({'message': 'Category not found!'}), 404
    db.session.delete(category_obj)
    db.session.commit()
    return jsonify({
        'status': 'Delete category success!'
    }), 200


def get_all_category():
    sql = text("SELECT * FROM category")
    result = db.session.execute(sql).fetchall()

    if not result:
        return jsonify({'message': 'No categories found!'}), 404

    rows = [dict(row._mapping) for row in result]
    return jsonify(rows), 200


def get_all_by_id(category_id: int):
    sql = text("SELECT * FROM category ")
    result = db.session.execute(sql, {"category_id": category_id}).fetchone()

    if not result:
        return jsonify({'error': 'Category not found!'}), 404

    row = dict(result._mapping)
    return jsonify(row), 200





