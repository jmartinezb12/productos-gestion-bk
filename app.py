from flask import Flask
from flask_migrate import Migrate
from models import db
from routes import create_routes  # Cambia a create_routes

app = Flask(__name__)
app.config.from_object('config.Config')

# Inicializa la base de datos
db.init_app(app)

# Inicializa las migraciones
migrate = Migrate(app, db)

# Registra las rutas
app.register_blueprint(create_routes())  # Registra el blueprint

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
