from flask import request, jsonify
from app import app, db
from sqlalchemy import func
from model.invoice import Invoice
from model.invoice_detail import InvoiceDetail

# -------------------- 1. Daily Sales --------------------
@app.get('/report/daily/<string:date_str>')
def report_daily(date_str):
    from datetime import datetime
    date = datetime.strptime(date_str, '%Y-%m-%d')
    sales = Invoice.query.filter(func.date(Invoice.date_time) == date.date()).all()
    total = sum([float(s.total) for s in sales])
    data = [{'invoice_id': s.id, 'customer_name': s.customer_name, 'total': float(s.total)} for s in sales]
    return jsonify({'date': date_str, 'total_sales': total, 'invoices': data}), 200

# -------------------- 2. Weekly Sales --------------------
@app.get('/report/weekly/<int:year>/<int:week_num>')
def report_weekly(year, week_num):
    # SQLite: strftime('%Y-%W')
    sales = Invoice.query.filter(func.strftime('%Y-%W', Invoice.date_time) == f"{year}-{week_num:02}").all()
    total = sum([float(s.total) for s in sales])
    data = [{'invoice_id': s.id, 'customer_name': s.customer_name, 'total': float(s.total)} for s in sales]
    return jsonify({'year': year, 'week': week_num, 'total_sales': total, 'invoices': data}), 200

# -------------------- 3. Monthly Sales --------------------
@app.get('/report/monthly/<int:year>/<int:month>')
def report_monthly(year, month):
    sales = Invoice.query.filter(
        func.extract('year', Invoice.date_time) == year,
        func.extract('month', Invoice.date_time) == month
    ).all()
    total = sum([float(s.total) for s in sales])
    data = [{'invoice_id': s.id, 'customer_name': s.customer_name, 'total': float(s.total)} for s in sales]
    return jsonify({'year': year, 'month': month, 'total_sales': total, 'invoices': data}), 200

# -------------------- 4. Sales by Criteria --------------------
@app.get('/report/saleby')
def report_saleby():
    """
    Query params example:
    ?product_name=Laptop&category=Electronics&user=John
    """
    product_name = request.args.get('product_name')
    category = request.args.get('category')
    user = request.args.get('user')

    query = InvoiceDetail.query.join(Invoice)

    if product_name:
        query = query.filter(InvoiceDetail.product_name == product_name)
    if user:
        query = query.filter(Invoice.customer_name == user)

    results = query.all()
    total = sum([float(r.subtotal) for r in results])
    data = [{'invoice_id': r.invoice_id, 'product_name': r.product_name,
             'quantity': r.quantity, 'subtotal': float(r.subtotal)} for r in results]

    return jsonify({'total_sales': total, 'details': data}), 200
