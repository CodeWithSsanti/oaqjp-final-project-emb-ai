import requests
import json

def emotion_detector(text_to_analyse):
    """
    Analiza las emociones del texto dado utilizando Watson NLP.
    
    Args:
        text_to_analyse (str): El texto a analizar
    
    Returns:
        dict: Un diccionario con los scores de emociones y la emoción dominante
    """
    # Verificar entrada vacía
    if not text_to_analyse or text_to_analyse.strip() == "":
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None
        }

    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    
    try:
        # Preparar el payload
        payload = {"raw_document": {"text": text_to_analyse}}
        
        # Realizar la solicitud POST
        response = requests.post(url, headers=headers, json=payload)
        
        # Verificar status_code
        if response.status_code != 200:
            return {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None
            }
        
        # Parsear la respuesta
        result = response.json()
        
        # Verificar que la respuesta contenga los datos necesarios
        if 'emotionPredictions' not in result or not result['emotionPredictions']:
            return {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None
            }
        
        # Extraer las emociones
        emotion_data = result["emotionPredictions"][0]["emotion"]
        
        # Crear el diccionario de emociones con valores redondeados
        emotions = {
            "anger": round(emotion_data.get("anger", 0), 2),
            "disgust": round(emotion_data.get("disgust", 0), 2),
            "fear": round(emotion_data.get("fear", 0), 2),
            "joy": round(emotion_data.get("joy", 0), 2),
            "sadness": round(emotion_data.get("sadness", 0), 2)
        }
        
        # Encontrar la emoción dominante
        dominant_emotion = max(emotions, key=emotions.get)
        
        # Agregar la emoción dominante al resultado
        emotions["dominant_emotion"] = dominant_emotion
        
        return emotions
        
    except requests.exceptions.RequestException as e:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None
        }
    except (KeyError, json.JSONDecodeError) as e:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None
        }