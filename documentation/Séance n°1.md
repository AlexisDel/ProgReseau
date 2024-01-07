# Séance n°1

### Objectifs :
- Configuration du robot :
    - Installation de Raspberry Pi OS
    - Installation des librairies nécessaires au projet
- Test des fonctionnalités du robot (via le script fourni)
- Mise en place de l'environnement de développement via SSH
- Début de la programmation

:warning: **Note** : Les "lessons" font référence aux tutoriels d'Adeept disponibles [ici](https://www.adeept.com/video/static1/itemsfile/901RaspTank%20Tutorials.zip), trouvables dans le dossier "*2 Basic course*".

## 1. Installation de Raspberry Pi OS
Référez-vous à : *Lesson 3 Installing and Configuring Raspberry Pi System*, Sections 3.1 - 3.6 (pages 1 à 19)

## 2. Installation des librairies nécessaires au projet
Récupérez le dossier de ressources et son contenu (disponible sur GitHub). Vous devriez avoir les fichiers suivants :

```
├── pi
    ├── home
        ├── ressources
            ├── setup.py
            ├── requirements.txt
            └── test.py
```

Exécutez :
```
sudo python3 /home/pi/ressources/setup.py
```
## 3. Test des fonctionnalités du Rasptank
Exécutez :
```
sudo python3 /home/pi/ressources/test.py
```
Suivez ensuite les instructions affichées à l'écran.

## 4. Mise en place de l'environnement de développement via SSH

:warning: Les réseaux `eduspot` et `edurom` isolent chaque appareil sur le réseau, rendant impossible la connexion SSH au Rasptank. Pour utiliser SSH, connectez-vous au réseau suivant :

SSID : `TP-Link_AC96`

Mot de passe : `rasptank`

:warning: Ce réseau n'a pas d'accès à Internet :confused:. Vous pouvez également utiliser le partage de connexion de votre téléphone.

Voir : [Remote Development using SSH](https://code.visualstudio.com/docs/remote/ssh)

**Note** : Assurez-vous d'activer le SSH sur le Raspberry Pi.

## 5. Commencer à programmer

Vous pouvez maintenant commencer à programmer votre robot. Suivez les leçons d'Adeept pour apprendre à utiliser les différents composants du robot :

- *Lesson 6 How to Control DC Motor*
- *Lesson 7 How to Control WS2812 LED*
- *Lesson 8 How to Control the Ultrasonic Module*
- *Lesson 9 How to Take a Photo with Raspberry Pi*
- *Lesson 13 How to Use the Tracking Module*

:warning: Ne pas toucher au Servos pour l'instant.