from flask import Flask, render_template, send_from_directory
import os

# Configuration correcte de Flask avec static/
app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def home():
    return render_template("index.html")

# Route pour servir manifest.json (facultatif mais conservé)
@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

# Route pour service-worker.js (si utilisé pour PWA/offline)
@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('.', 'service-worker.js', mimetype='application/javascript')

@app.route('/offline.html')
def offline():
    return render_template('offline.html')

# ✅ Route de test pour voir le contenu de page_state.txt dans le navigateur
@app.route('/etat')
def etat():
    try:
        with open(os.path.join(app.static_folder, 'page_state.txt'), 'r') as f:
            contenu = f.read().strip()
        return f"Page actuelle : {contenu}"
    except FileNotFoundError:
        return "Fichier page_state.txt introuvable", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000, use_reloader=False)
    print("[DEBUG] static_folder =", app.static_folder)


