# Séance n°1

### Objectifs :
- Configuration du robot :
    - Installation de Raspberry Pi OS
    - Installation des librairies nécessaires au projet
- Mise en place de l'environnement de développement via SSH
- Début de la programmation

:warning: **Note** : Les "lessons" font référence aux tutoriels d'Adeept disponibles [ici](https://www.adeept.com/video/static1/itemsfile/901RaspTank%20Tutorials.zip), trouvables dans le dossier "*2 Basic course*"

## 1. Installation de Raspberry Pi OS

- Téléchargez [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
- Flashez la carte SD :
    - Choose Device : Raspberry Pi 4  
    ![Raspberry Pi Imager](/documentation/images/choose_device.png)
    - Choose OS : Raspberry Pi OS (Legacy, 32-bit)  
    ![Raspberry Pi Imager](/documentation/images/choose_os.png)
    - Choose Storage :  
    ![Raspberry Pi Imager](/documentation/images/choose_storage.png)
    - Ensuite, cliquez sur *Next* :
        - Would you like to apply OS customization settings? : No
        - All existing data on '...' will be erased? : Yes

- Insérez la carte SD dans le Raspberry Pi  
![](images/sd_slot.png)

:white_check_mark: Vous pouvez maintenant allumer le Raspberry Pi en branchant l'alimentation et le câble HDMI.

## 2. Configuration du Raspberry Pi

- Ouvrez la configuration du Raspberry Pi  
![](images/select_rpi_config.png)

- Activez l'I2C et le SSH  
![](images/rpi_config.png)

:white_check_mark: Vous pouvez maintenant redémarrer le Raspberry Pi

## 3. Installation des librairies nécessaires au projet

:warning: Connectez-vous à un réseau Wifi avant de poursuivre

Récupérez le dossier src du rasptank et son contenu [disponible sur GitHub](../src/rasptank/). Vous devriez avoir les fichiers suivants :

```
├── pi
    ├── home
        ├── rasptank
            ├── setup.py
            ├── requirements.txt
            ├── InfraLib.txt
            └── test.py
```

Vous pouvez récupérer les fichiers via :

```
git clone https://github.com/AlexisDel/ProgReseau
```

Exécutez :
```
sudo python3 /home/pi/ProgReseau/src/rasptank/setup.py
```
Le Raspberry va redémarrer une fois l'installation terminée

## 4. Mise en place de l'environnement de développement via SSH

:warning: Les réseaux `eduspot` et `edurom` isolent chaque appareil sur le réseau, rendant impossible la connexion SSH au Rasptank. Pour utiliser SSH, connectez-vous au réseau suivant :

SSID : `TP-Link_AC96`

Mot de passe : `rasptank`

Ce réseau n'a pas d'accès à Internet :confused:. Vous pouvez également utiliser le partage de connexion de votre téléphone.

Voir : [Remote Development using SSH](https://code.visualstudio.com/docs/remote/ssh)

**Note** : Assurez-vous d'activer le SSH sur le Raspberry Pi

## 5. Commencer à programmer

Vous pouvez maintenant commencer à programmer votre robot. Suivez les leçons d'Adeept pour apprendre à utiliser les différents composants du robot :

- *Lesson 6 How to Control DC Motor*
- *Lesson 7 How to Control WS2812 LED*
- *Lesson 8 How to Control the Ultrasonic Module*
- *Lesson 13 How to Use the Tracking Module*

:warning: Ne pas toucher au Servos pour l'instant

:information_source: Pour commencer à programmer le robot, il est recommandé de créer des fonctions de base afin de contrôler votre robot, telles que `move()`, `enableLED()`, etc. Cela vous permettra ensuite d'intégrer facilement la communication avec la télécommande. Par exemple, si je reçois `MoveLeft` de la télécommande, alors j'appelle `move('Left')`.