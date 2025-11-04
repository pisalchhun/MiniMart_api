from datetime import datetime

from app import app, db
from flask import request, jsonify
from sqlalchemy import text
from model.invoice import Invoice

@app.get('/invoice/list')
def get_invoice():
    return get_all_invoice()


@app.get('/invoice/list/<int:product_id>')
def get_invoice_by_id(invoice_id):
    return get_all_by_id(invoice_id)


@app.post('/invoice/create')
def create_invoice():
    invoice = request.get_json()
    if not invoice:
        return jsonify({'message': 'No invoice data provided!'}), 400
    if not invoice.get('customer_name'):
        return jsonify({'message': 'Customer name is required!'}), 400
    if not invoice.get('date_time'):
        return jsonify({'message': 'Date is required!'}), 400
    if not invoice.get('total'):
        return jsonify({'message': 'Total is required!'}), 400

    customer_name = invoice.get('customer_name')
    total = invoice.get('total')
    date_time_str = invoice.get('date_time')
    date_time = datetime.strptime(date_time_str, '%Y-%m-%d')
    invoice_obj = Invoice(
        customer_name=customer_name,
        date_time=date_time,
        total= total
    )

    db.session.add(invoice_obj)
    db.session.commit()
    return jsonify({
        'status': 'Create invoice success!'
    }), 201


def get_all_invoice():
    sql = text("SELECT * FROM invoice")
    result = db.session.execute(sql).fetchall()

    if not result:
        return jsonify({'message': 'No invoice found!'}), 404

    rows = [dict(row._mapping) for row in result]
    return jsonify(rows), 200


def get_all_by_id(invoice_id: int):
    sql = text("SELECT * FROM invoice ")
    result = db.session.execute(sql, {"category_id": invoice_id}).fetchone()

    if not result:
        return jsonify({'error': 'Invoice not found!'}), 404

    row = dict(result._mapping)
    return jsonify(row), 200
