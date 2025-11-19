from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialiser la base de données
    db.init_app(app)
    
    # Créer le dossier d'uploads s'il n'existe pas
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Importer et enregistrer le blueprint
    from .routes.main import main_blueprint
    app.register_blueprint(main_blueprint)
    
    # Créer les tables de la base de données
    with app.app_context():
        db.create_all()
    
    return app