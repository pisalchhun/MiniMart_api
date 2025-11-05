from flask import request, jsonify
from app import app, db
from model.invoice_detail import InvoiceDetail
from model.invoice import Invoice

# 🧮 Helper function to recalc invoice total
def update_invoice_total(invoice_id):
    details = InvoiceDetail.query.filter_by(invoice_id=invoice_id).all()
    total = sum([float(d.subtotal) for d in details])
    invoice = Invoice.query.get(invoice_id)
    if invoice:
        invoice.total = total
        db.session.commit()


# ✅ 1. Create Sale Detail
@app.post('/invoice-detail/create')
def create_invoice_detail():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided!'}), 400

    required_fields = ['invoice_id', 'product_name', 'quantity', 'price']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'{field} is required!'}), 400

    invoice_id = data['invoice_id']
    product_name = data['product_name']
    quantity = int(data['quantity'])
    price = float(data['price'])
    subtotal = quantity * price

    detail = InvoiceDetail(
        invoice_id=invoice_id,
        product_name=product_name,
        quantity=quantity,
        price=price,
        subtotal=subtotal
    )

    db.session.add(detail)
    db.session.commit()

    # update invoice total
    update_invoice_total(invoice_id)

    return jsonify({'message': 'Sale detail added and invoice total updated!'}), 201


# ✅ 2. Update Sale Detail
@app.put('/invoice-detail/update/<int:id>')
def update_invoice_detail(id):
    data = request.get_json()
    detail = InvoiceDetail.query.get(id)

    if not detail:
        return jsonify({'message': 'Sale detail not found!'}), 404

    detail.product_name = data.get('product_name', detail.product_name)
    detail.quantity = int(data.get('quantity', detail.quantity))
    detail.price = float(data.get('price', detail.price))
    detail.subtotal = detail.quantity * detail.price

    db.session.commit()

    # update invoice total
    update_invoice_total(detail.invoice_id)

    return jsonify({'message': 'Sale detail updated and invoice total recalculated!'}), 200


# ✅ 3. Delete Sale Detail
@app.delete('/invoice-detail/delete/<int:id>')
def delete_invoice_detail(id):
    detail = InvoiceDetail.query.get(id)
    if not detail:
        return jsonify({'message': 'Sale detail not found!'}), 404

    invoice_id = detail.invoice_id
    db.session.delete(detail)
    db.session.commit()

    # update invoice total
    update_invoice_total(invoice_id)

    return jsonify({'message': 'Sale detail deleted and invoice total updated!'}), 200


# ✅ 4. List Sale Details for an Invoice
@app.get('/invoice-detail/list/<int:invoice_id>')
def get_invoice_details(invoice_id):
    details = InvoiceDetail.query.filter_by(invoice_id=invoice_id).all()

    if not details:
        return jsonify({'message': 'No sale details found for this invoice!'}), 404

    data = []
    for d in details:
        data.append({
            'id': d.id,
            'invoice_id': d.invoice_id,
            'product_name': d.product_name,
            'quantity': d.quantity,
            'price': float(d.price),
            'subtotal': float(d.subtotal)
        })

    return jsonify(data), 200
