from deepface import DeepFace
import cv2

class AgePredictor:
    def __init__(self):
        self.allowed_extensions = {'png', 'jpg', 'jpeg'}

    def allowed_file(self, filename, allowed_extensions):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    def predict_age(self, image_path):
        try:
            # Utilisation de DeepFace pour la prédiction d'âge
            result = DeepFace.analyze(img_path=image_path, 
                                    actions=['age', 'gender', 'emotion'],
                                    enforce_detection=False)
            
            # Récupérer l'âge prédit
            age = int(result[0]['age'])
            # La confiance n'est pas directement fournie, on peut utiliser un score de confiance factice
            confidence = 0.8  # Valeur factice, à ajuster selon vos besoins
            
            return age, confidence
            
        except Exception as e:
            print(f"Erreur lors de la prédiction: {str(e)}")
            return None, 0