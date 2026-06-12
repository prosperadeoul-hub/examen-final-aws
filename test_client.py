import os
import requests
import json
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupération de l'URL CloudFront exigée par la consigne de l'examen
URL_INGESTION = os.getenv("CLOUDFRONT_INGESTION_URL")

def envoyer_donnies_valides():
    print("Envoi d'un jeu de données VALIDES (7 mesures)")
    
    # Payload contenant exactement 7 mesures structurées
    payload = {
        "measures": [
            {"sensor_id": "capteur-01", "temperature": 24.5, "status": "OK"},
            {"sensor_id": "capteur-02", "temperature": 26.2, "status": "OK"},
            {"sensor_id": "capteur-03", "temperature": 85.0, "status": "ERROR"}, 
            {"sensor_id": "capteur-04", "temperature": 23.1, "status": "OK"},
            {"sensor_id": "capteur-05", "temperature": 22.8, "status": "OK"},
            {"sensor_id": "capteur-06", "temperature": 91.4, "status": "ERROR"},
            {"sensor_id": "capteur-07", "temperature": 25.0, "status": "OK"}
        ]
    }
    
    try:
        print(f"Cible : {URL_INGESTION}")
        response = requests.post(URL_INGESTION, json=payload)
        
        # Interception et affichage de la réponse d'AWS
        print(f"Statut HTTP reçu : {response.status_code}") 
        print(f"Réponse d'AWS : {response.text}\n")
    except Exception as e:
        print(f"Erreur lors de la requête : {e}\n")

def envoyer_donnies_corrompues():
    print("--- Envoi d'un jeu de données CORROMPUES (Test de validation) ---")

    # Payload invalide pour tester la robustesse de la Lambda
    payload_invalide = {
        "measures": [
            {"sensor_id": "capteur-08", "status": "OK"},
            {"sensor_id": "capteur-09", "temperature": "PasUneTemperature", "status": "ERROR"}
        ]
    }
    
    try:
        print(f"Cible : {URL_INGESTION}")
        response = requests.post(URL_INGESTION, json=payload_invalide)
        print(f"Statut HTTP reçu : {response.status_code}")
        print(f"Réponse d'AWS : {response.text}\n")
    except Exception as e:
        print(f"Erreur interceptée : {e}\n")

if __name__ == "__main__":
    print("Script client prêt pour les tests post-déploiement.\n")
    
    if not URL_INGESTION:
        print("Erreur : La variable 'CloudFrontIngestionURL' n'est pas configurée dans ton fichier .env")
    else:
        envoyer_donnies_valides()
        envoyer_donnies_corrompues()