import re
import io
import base64
import pyqrcode
from flask import Flask, request, jsonify
from flask_cors import CORS

# ────────────────────────────────────────────────
# Initialisation de l'application Flask
# CORS est activé pour autoriser les requêtes
# provenant du frontend VueJS (port 5173)
# ────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)

# Expression régulière de validation d'URL.
#
# Problèmes de la regex originale (main.py) :
#   1. Elle n'acceptait pas les tirets dans les noms de
#      domaine (ex: portefolio-kimberleyanique.my.canva.site)
#   2. Elle ne gérait qu'un seul sous-domaine (ex: www.example.com)
#      et échouait pour les domaines à plusieurs niveaux
#      (ex: something.my.canva.site)
#
# Nouvelle regex :
#   ^(https?://)?         → protocole optionnel (http ou https)
#   (([a-zA-Z0-9\-]+\.)+  → un ou plusieurs labels (alphanum + tirets) suivis d'un point
#   [a-zA-Z]{2,})         → TLD obligatoire d'au moins 2 lettres (ex: .com, .site, .fr)
#   ([/?#].*)?$           → chemin / query string / fragment optionnels
URL_REGEX = re.compile(
    r'^(https?://)?(([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,})([/?#].*)?$'
)


def verifier_url(url: str) -> bool:
    """Vérifie qu'une URL est valide selon URL_REGEX.

    Args:
        url: La chaîne de caractères à valider.

    Returns:
        True si l'URL est considérée valide, False sinon.
    """
    return bool(URL_REGEX.match(url))


@app.route('/api/generate', methods=['POST'])
def generer_qrcode():
    """Endpoint principal : génère un QR code à partir d'une URL.

    Corps de la requête (JSON) :
        { "url": "https://example.com" }

    Réponse (JSON) :
        { "image": "data:image/png;base64,..." }  → succès
        { "error": "..." }                        → erreur (400)
    """
    donnees = request.get_json()

    # Récupération et nettoyage de l'URL fournie
    url = donnees.get('url', '').strip()

    if not url:
        return jsonify({'error': 'URL manquante'}), 400

    if not verifier_url(url):
        return jsonify({'error': 'URL invalide'}), 400

    # Génération du QR code en mémoire avec pyqrcode
    # scale=10 → chaque module du QR code fait 10×10 pixels
    qrcode = pyqrcode.create(url)
    tampon = io.BytesIO()
    qrcode.png(tampon, scale=10)
    tampon.seek(0)

    # Encodage en base64 pour être transmis dans la réponse JSON
    encoded = base64.b64encode(tampon.read()).decode('utf-8')

    return jsonify({'image': f'data:image/png;base64,{encoded}'})


if __name__ == '__main__':
    # Lancement en mode debug sur le port 5000
    app.run(debug=True, port=5000)
