# Idées : Télécommande

Ici vous êtes totalement libre, votre télécommande doit cependant être capable d'afficher le stream vidéo de la webcam du robot et d'envoyer des commandes au robot. 

## Une première version

:bulb: Je vous conseille dans un premier temps de faire un truc très simple sans interface graphique afin de tester la communication entre le robot et la télécommande. Vous pourrez ainsi commencer à développer les fonctionnalités de base du robot (déplacement, tirs, ...) 

## Quelques idées

<img title="" src="../images/controller_tk.png" alt="" width="435" data-align="inline">

Il existe de nombreuse bibliothèque graphique que vous pouvez utilisé pour créer votre télécommande, en voici une liste non exhaustive:

###### Tkinter :star:

Avantage : 

- Tkinter est sans doute la bibliothèque graphique python la plus connu, il y a donc beaucoup de documentation sur internet.

Inconvénient:

- Tkinter n'est pas optimiser pour afficher de la vidéo, ce qui fait que sur un Raspberry, d'après mes tests, la vidéo ne dépasse pas 15-20 fps ce qui est problématique dans notre cas. 
  
  :information_source: Cependant si vous avez prévu d'utiliser votre PC portable en tant que télécommande cela fonctionne correctement à 30 fps.

###### PyQt5

Avantage : 

- Lecture de vidéo fluide sur un Raspberry, 45 fps constant d'après mes tests.

Inconvénient:

- Plus compliqué à utiliser que Tkinter.

###### GTK (:warning: pas testé)

Avantage :

- Lecture de vidéo sans doute fluide sur Raspberry (c'est ce qui est utilisé par OpenCV)

Inconvénient:

- Plus compliqué à utiliser que Tkinter.

### 2 Applications GUI

Une autre idée serait d'utiliser la fonction `imshow` d'OpenCV pour afficher le retour vidéo et faire un autre programme avec Tkinter pour les boutons de la télécommande.

Avantage : 

- Fluidité de la vidéo grâce à `imshow` + simplicité de Tkinter.

Inconvénient: 

- 2 fenêtres différentes

## Ajouts

Comme indiqué précédemment vous êtes entièrement libre pour la télécommande donc si vous voulez par exemple utiliser une mannette de Playstation ou d'Xbox au lieu de codé une application GUI avec des boutons faites le.

:warning: Je vous met tout de même en garde car le projet est assez dense il est donc fortement recommander de finir la partie obligatoire du projet avant d'implémenter ce genre de fonctionnalité.
