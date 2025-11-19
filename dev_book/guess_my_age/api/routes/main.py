from flask import Blueprint, render_template, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from ..models import db, Prediction
from ..controllers.age_predictor import AgePredictor

# Créer le blueprint
bp = Blueprint('main', __name__)
age_predictor = AgePredictor()

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier fourni'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné'}), 400
    
    if file and age_predictor.allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Prédire l'âge
        predicted_age, confidence = age_predictor.predict_age(filepath)
        
        if predicted_age is None:
            return jsonify({'error': 'Aucun visage détecté'}), 400
        
        # Enregistrer la prédiction dans la base de données
        prediction = Prediction(
            filename=filename,
            predicted_age=predicted_age,
            confidence=confidence
        )
        db.session.add(prediction)
        db.session.commit()
        
        return jsonify({
            'age': predicted_age,
            'confidence': confidence,
            'image_url': f'/uploads/{filename}'
        })
    
    return jsonify({'error': 'Format de fichier non supporté'}), 400

# Exporter le blueprint
main_blueprint = bp