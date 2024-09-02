from flask import Blueprint, jsonify, request
from models import db, Product, Transaction
from pyzbar.pyzbar import decode
from PIL import Image
from flask_cors import CORS
import io
import json  # Asegúrate de importar json

def create_routes():
    app = Blueprint('app', __name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    @app.route('/products', methods=['POST'])
    def add_product():
        data = request.json
        new_product = Product(name=data['name'], quantity=data['quantity'])
        db.session.add(new_product)
        db.session.commit()
        return jsonify(new_product.to_dict()), 201

    @app.route('/products', methods=['GET'])
    def get_products():
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products])

    @app.route('/products/<int:product_id>', methods=['GET'])
    def get_product(product_id):
        product = Product.query.get_or_404(product_id)
        return jsonify({
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'is_defective': product.is_defective
        }), 200

    @app.route('/products/<int:product_id>/defective', methods=['PATCH'])
    def mark_defective(product_id):
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        product.is_defective = data.get('is_defective', product.is_defective)
        db.session.commit()
        return jsonify({'message': 'Product defect status updated successfully'}), 200

    @app.route('/products/<int:product_id>', methods=['PUT'])
    def update_product(product_id):
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        product.name = data['name']
        product.quantity = data['quantity']
        product.is_defective = data.get('is_defective', product.is_defective)
        db.session.commit()
        return jsonify({'message': 'Product updated successfully'})

    @app.route('/products/<int:product_id>', methods=['DELETE'])
    def delete_product(product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'})

    @app.route('/transactions', methods=['POST'])
    def create_transaction():
        data = request.get_json()
        product = Product.query.get_or_404(data['product_id'])
        transaction = Transaction(product_id=product.id, quantity=data['quantity'], type=data['type'])
        
        if data['type'] == 'entry':
            product.quantity += data['quantity']
        elif data['type'] == 'exit':
            if product.quantity >= data['quantity']:
                product.quantity -= data['quantity']
            else:
                return jsonify({'error': 'Not enough stock'}), 400
        
        db.session.add(transaction)
        db.session.commit()
        return jsonify({'message': 'Transaction recorded successfully'}), 201

    @app.route('/transactions', methods=['GET'])
    def get_transactions():
        transactions = Transaction.query.all()
        return jsonify([{
            'id': txn.id,
            'product_id': txn.product_id,
            'quantity': txn.quantity,
            'type': txn.type,
            'timestamp': txn.timestamp
        } for txn in transactions]), 200

    @app.route('/process_qr', methods=['POST'])
    def process_qr():
        data = request.get_json()
        qr_data = data.get('qr_data')
        
        product_id = qr_data.get('product_id')
        action = qr_data.get('action')  # 'entry' o 'exit'
        quantity = qr_data.get('quantity', 1)  # cantidad por defecto
        
        product = Product.query.get_or_404(product_id)
        
        if action == 'entry':
            product.quantity += quantity
        elif action == 'exit':
            if product.quantity >= quantity:
                product.quantity -= quantity
            else:
                return jsonify({'error': 'Not enough stock'}), 400
        else:
            return jsonify({'error': 'Invalid action'}), 400
        
        transaction = Transaction(product_id=product.id, quantity=quantity, type=action)
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({'message': f'Transaction {action} recorded successfully'}), 201

    @app.route('/upload_qr', methods=['POST'])
    def upload_qr():
        file = request.files.get('file')
        if not file:
            return jsonify({'error': 'No file provided'}), 400
        
        image = Image.open(io.BytesIO(file.read()))
        decoded_objects = decode(image)
        
        if not decoded_objects:
            return jsonify({'error': 'No QR code found'}), 400
        
        qr_data = decoded_objects[0].data.decode('utf-8')
        qr_json = json.loads(qr_data)
        
        return jsonify({'message': 'QR processed successfully', 'data': qr_json}), 200

    return app
