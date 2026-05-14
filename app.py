from flask import Flask
from flask_wtf.csrf import CSRFProtect
from routes.public import public_bp
from routes.auth import auth_bp
from routes.admin import admin_bp
import database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'OVRFLOW_PREMIUM_2026_SECURE_KEY'
csrf = CSRFProtect(app)

# Registro de Blueprints
app.register_blueprint(public_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    database.crear_tablas() # Asegura que la DB esté lista
    app.run(debug=True)