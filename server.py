"""
Este módulo implementa un servidor Flask para detectar emociones
a partir de un texto ingresado por el usuario.
"""

import logging
from flask import Flask, request, jsonify, render_template
from EmotionDetection import emotion_detector

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

def create_response(message, code):
    """Creates a consistent JSON response for invalid inputs."""
    return jsonify({
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None,
        'message': message
    }), code

@app.route("/", methods=["GET"])
def home():
    """Renders the home page."""
    return render_template('index.html')

@app.route("/emotionDetector", methods=["GET"])
def emotion_detector_route():
    """Handles emotion detection for the given text input."""
    text = request.args.get('textToAnalyze')
    app.logger.debug("Texto recibido: '%s'", text)

    if not text or text.strip() == "":
        # Respond with a valid message for empty input
        return create_response('Texto invalido, Por favor, intentalo de nuevo', 200)

    # Call the emotion detection function
    result = emotion_detector(text)
    app.logger.debug("Resultado del analisis: %s", result)

    if result.get('dominant_emotion') is None:
        return create_response('Texto invalido, Por favor, intentalo de nuevo', 200)

    # Add a success message if analysis is valid
    result['message'] = 'Analisis completado exitosamente'
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
