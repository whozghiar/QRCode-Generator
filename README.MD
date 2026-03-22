# QR Code Generator

Générateur de QR code en ligne : entrez une URL valide, obtenez instantanément votre QR code et téléchargez-le au format PNG.

---

## Table des matières

- [Guide utilisateur](#guide-utilisateur)
  - [Démarrer l'application](#démarrer-lapplication)
  - [Utiliser l'application](#utiliser-lapplication)
- [Guide développeur](#guide-développeur)
  - [Architecture](#architecture)
  - [Backend Flask](#backend-flask)
  - [Frontend VueJS](#frontend-vuejs)
  - [Validation des URL](#validation-des-url)

---

## Guide utilisateur

### Démarrer l'application

> **Prérequis :** Python 3.x et Node.js doivent être installés.

**Étape 1 — Installer les dépendances Python (une seule fois) :**

```bash
cd backend
pip install -r requirements.txt
```

**Étape 2 — Ouvrir deux terminaux :**

| Terminal | Commande | Rôle |
|---|---|---|
| Terminal 1 | `cd backend && python app.py` | Démarre le serveur Flask (port 5000) |
| Terminal 2 | `cd frontend && npm install && npm run dev` | Démarre l'interface web (port 5173) |

**Étape 3 — Ouvrir le navigateur à l'adresse :**

```
http://localhost:5173
```

---

### Utiliser l'application

#### 1. État initial

Au chargement, le champ URL est vide et le bouton **▶ GÉNÉRER** est désactivé.

![État initial de l'application](docs/screenshots/etat_initial.png)

---

#### 2. Saisir une URL invalide

Si l'URL saisie n'est pas reconnue comme valide (ex : `hello world`, texte sans domaine), le badge passe en rouge **✗ INVALIDE** et le bouton reste inaccessible.

![URL invalide — bouton désactivé](docs/screenshots/url_invalide.png)

---

#### 3. Saisir une URL valide

Dès qu'une URL valide est détectée (ex : `https://github.com/whozghiar/QRCode-Generator`), le badge passe en jaune **✓ VALIDE** et le bouton **▶ GÉNÉRER** s'active.

![URL valide — bouton actif](docs/screenshots/url_valide.png)

---

#### 4. Générer et télécharger le QR code

Cliquez sur **▶ GÉNÉRER**. Le QR code apparaît en quelques instants.  
Cliquez ensuite sur **↓ TÉLÉCHARGER (.PNG)** pour sauvegarder l'image sur votre ordinateur.

![QR code généré avec bouton de téléchargement](docs/screenshots/qrcode_genere.png)

---

## Guide développeur

### Architecture

```
QRCode-Generator/
│
├── main.py                  # Application originale Tkinter (conservée)
├── src/
│   └── qrcode.ico           # Icône originale
│
├── backend/                 # Serveur API Python
│   ├── app.py               # Application Flask
│   └── requirements.txt     # Dépendances Python
│
├── frontend/                # Interface web VueJS
│   ├── index.html           # Point d'entrée HTML
│   ├── vite.config.js       # Configuration Vite (proxy API)
│   ├── package.json         # Dépendances Node.js
│   └── src/
│       ├── main.js          # Montage de l'application Vue
│       ├── style.css        # Styles globaux (design brutaliste)
│       └── App.vue          # Composant principal
│
└── docs/
    └── screenshots/         # Captures d'écran pour la documentation
```

---

### Backend Flask

**Fichier :** `backend/app.py`

Le backend expose un unique endpoint REST :

| Méthode | Route | Description |
|---|---|---|
| `POST` | `/api/generate` | Génère un QR code à partir d'une URL |

**Corps de la requête :**
```json
{ "url": "https://example.com" }
```

**Réponses :**
```json
// Succès (200)
{ "image": "data:image/png;base64,..." }

// Erreur (400)
{ "error": "URL invalide" }
```

**Dépendances :**

| Paquet | Rôle |
|---|---|
| `flask` | Serveur web et routage |
| `flask-cors` | Autorise les requêtes cross-origin du frontend |
| `pyqrcode` | Génération du QR code (même librairie que `main.py`) |
| `pypng` | Export du QR code en PNG |

---

### Frontend VueJS

**Fichier :** `frontend/src/App.vue`

Le composant unique gère l'intégralité de l'interface :

| Référence Vue | Type | Rôle |
|---|---|---|
| `url` | `ref` | Valeur du champ URL |
| `qrImage` | `ref` | Image base64 reçue du backend |
| `loading` | `ref` | État de chargement pendant la requête |
| `error` | `ref` | Message d'erreur à afficher |
| `isValid` | `computed` | `true` si l'URL passe la regex |
| `statusLabel` | `computed` | Texte du badge (VALIDE / INVALIDE / EN ATTENTE) |

Le proxy Vite (`vite.config.js`) redirige automatiquement tous les appels `/api/*` vers `http://localhost:5000`, évitant ainsi tout problème CORS en développement.

---

### Validation des URL

La validation est effectuée **des deux côtés** (frontend et backend) avec la même expression régulière :

```
^(https?://)?(([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,})([/?#].*)?$
```

| Partie | Description |
|---|---|
| `^(https?://)?` | Protocole HTTP/HTTPS optionnel |
| `(([a-zA-Z0-9\-]+\.)+` | Un ou plusieurs labels (alphanum + tirets) séparés par des points |
| `[a-zA-Z]{2,})` | TLD obligatoire d'au moins 2 lettres (`.com`, `.site`, `.fr`…) |
| `([/?#].*)?$` | Chemin, query string ou fragment optionnels |

**Exemples d'URL valides :**
- `https://github.com/whozghiar/QRCode-Generator` ✅
- `https://some-project.my.canva.site/page` ✅ (tirets + sous-domaines multiples)
- `google.fr`
- `http://www.example.co.uk/page?q=test`

**Exemples d'URL invalides :**
- `hello world` (espace)
- `localhost` (pas de TLD)
- `ftp://example.com` (protocole non HTTP)

---

## Auteur

[Whozghiar](https://github.com/whozghiar)
