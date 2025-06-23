from Electronique import initialiser_gpio, nettoyer_gpio, personne_detectee, allumer_led, eteindre_led
from Informatique import lancer_message_introduction, changer_page
from flask_cors import CORS
from flask import Flask, request, jsonify, make_response
import threading
import time
import os
import requests
import base64
import sys
import uuid
import json

app = Flask(__name__)
CORS(app)

SERVEUR_DISTANT_ASK_URL = "http://192.168.252.230:8000/ask"  # <-- Adresse du backend (Rasa/TTS)

# Initialisation GPIO
try:
    initialiser_gpio()
except RuntimeError as e:
    print(f"[GPIO] ❌ Erreur d'initialisation GPIO : {e}")
    sys.exit(1)

# Thread de détection
def detection_loop():
    print("[MAIN] 🎯 Attente de détection...")
    while True:
        try:
            if personne_detectee():
                print("[MAIN] ✅ Présence détectée !")
                allumer_led()
                time.sleep(3)

                lancer_message_introduction()
                changer_page("interaction")
            else:
                eteindre_led()
            time.sleep(0.5)
        except Exception as e:
            print(f"[MAIN] ⚠️ Erreur dans la boucle de détection : {e}")
            time.sleep(1)

# ✅ Gère la requête préliminaire OPTIONS (CORS)
@app.route("/ask", methods=["POST", "OPTIONS"])
def ask_question():
    if request.method == "OPTIONS":
        # Réponse CORS pour la requête preflight
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    data = request.get_json()
    question = data.get("message", "").strip()
    if not question:
        return jsonify({"error": "Aucune question reçue"}), 400

    print(f"[MAIN] 📨 Envoi question au serveur distant : {question}")

    try:
        response = requests.post(SERVEUR_DISTANT_ASK_URL, json={"message": question}, timeout=15)

        if response.status_code != 200:
            print(f"[MAIN] ❌ Erreur du serveur distant : code {response.status_code}")
            return jsonify({"error": "Erreur serveur distant"}), 500

        data = response.json()

        # Audio reçu ?
        audio_b64 = data.get("audio")
        result = jsonify({
            "status": "ok",
            "audio": audio_b64 if audio_b64 else None
        })
        result.headers['Access-Control-Allow-Origin'] = '*'  # ✅ Autorise le frontend
        return result

    except Exception as e:
        print(f"[MAIN] ❌ Exception appel serveur distant : {e}")
        error_response = jsonify({"error": str(e)})
        error_response.headers['Access-Control-Allow-Origin'] = '*'
        return error_response, 500

if __name__ == "__main__":
    try:
        thread = threading.Thread(target=detection_loop, daemon=True)
        thread.start()

        print("[MAIN] 🚀 Serveur Flask lancé sur le port 5000")
        app.run(host="0.0.0.0", port=5000)
    finally:
        nettoyer_gpio()
        print("[MAIN] 🔌 GPIO nettoyé à la sortie.")
