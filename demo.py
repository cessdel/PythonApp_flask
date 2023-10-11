from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///helados.db'
db = SQLAlchemy(app)

# Definición del modelo de la tabla "sabores"
class Sabores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sabor = db.Column(db.String(255), nullable=False)

# Crear la tabla en la base de datos (solo se necesita una vez)
with app.app_context():
    db.create_all()

# Ruta para crear un nuevo sabor de helado en la base de datos
@app.route('/create', methods=['POST'])
def create_sabor():
    data = request.get_json()
    sabor = Sabores(sabor=data['sabor'])
    db.session.add(sabor)
    db.session.commit()
    return jsonify({'message': 'Sabor de helado creado exitosamente'}), 201

# Ruta para obtener todos los sabores de helado en la base de datos
@app.route('/sabores', methods=['GET'])
def get_sabores():
    sabores = Sabores.query.all()
    sabores_list = [{'id': s.id, 'sabor': s.sabor} for s in sabores]
    return jsonify(sabores_list)

# Ruta para actualizar un sabor de helado por su ID
@app.route('/update/<int:id>', methods=['PUT'])
def update_sabor(id):
    data = request.get_json()
    sabor = Sabores.query.get(id)
    if sabor:
        sabor.sabor = data['sabor']
        db.session.commit()
        return jsonify({'message': 'Sabor de helado actualizado exitosamente'})
    else:
        return jsonify({'message': 'Sabor de helado no encontrado'}), 404

# Ruta para eliminar un sabor de helado por su ID
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_sabor(id):
    sabor = Sabores.query.get(id)
    if sabor:
        db.session.delete(sabor)
        db.session.commit()
        return jsonify({'message': 'Sabor de helado eliminado exitosamente'})
    else:
        return jsonify({'message': 'Sabor de helado no encontrado'}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
