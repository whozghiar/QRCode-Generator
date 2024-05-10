# QR Code Generator

Ce programme permet de générer un QR Code à partir d'une URL.

## Prérequis

Avant de pouvoir utiliser ce programme, vous devez installer les modules suivants:

* tkinter
* pyqrcode
* png
* re

Vous pouvez les installer en utilisant `pip` en exécutant les commandes suivantes:

```
pip install tkinter
pip install pyqrcode
pip install png
pip install re
```

## Utilisation

Pour utiliser ce programme :  
 * Téléchargez l'archive RAR.
 * Extraire le contenu de l'archive
 * Lancer "main.exe"

Une fenêtre s'ouvrira alors avec un emplacement pour entrer une URL. Entrez une URL valide et cliquez sur le bouton "Générer" pour générer le QR Code. 
Vous serez invité à enregistrer le QR Code dans un fichier PNG. 
Une fois enregistré, le QR Code s'affichera dans une boîte de message.

## Notes

* Le bouton "Générer" n'est actif que si l'URL entrée est valide.
* Le QR Code est généré à l'aide du module `pyqrcode` et enregistré dans un fichier PNG à l'aide du module `png`.
* La validation de l'URL est effectuée à l'aide de l'expression régulière dans le module `re`.

## Auteur

[Whozghiar]https://github.com/whozghiar
