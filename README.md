# Projet M1 IoT

## Présentation

Le but de ce projet est de construire et programmer un petit robot afin de s'affronter lors de partie de *World of Rasptank*.

### *World of Rasptank*

Dans ce jeu, il y a 2 équipes, une équipe bleue et une équipe rouge, les binômes sont répartis de manière équitable dans chacune des équipes. Chaque équipe possède une base. Le but est d'aller capturer le drapeau se trouvant au milieu du terrain et de le ramener dans sa base.

Pour capturer le drapeau, il vous suffit de rester 5 secondes dans la zone de capture. 

:warning: Attention :

- Si vous êtes détenteur du drapeau et que vous vous faites tirer dessus, vous perdrez le drapeau, celui-ci est alors retourné à la zone de capture.
- Si vous êtes en train de capturer le drapeau que vous vous faites tirer dessus, la capture sera annulée, il vous faudra alors sortir de la zone et y retourner pour commencer une nouvelle capture.

Pour déposer votre drapeau dans votre base, il vous suffit de vous rapprocher assez près de la caméra présente dans votre base. Une équipe remporte la partie si elle ramène 3 drapeaux dans son camps.

## Consignes

Afin de réaliser ce projet vous serez en binôme. Afin de réaliser ce projet le matériel suivant vous ait fourni:

- 2 Raspberry Pi 4
- 1 kit Rasptank

Le Raspberry Pi est un petit ordinateur capable de faire tourner un OS complet tel que linux, il est donc possible par exemple de faire tourner des programmes python dessus. Le Raspberry Pi 4 (celui que vous utiliserez dans le cadre de ce projet) est doté d'une puce WiFi qui va vous permettre de le contrôler à distance.

<img title="" src="images/rpi4.png" alt="drawing" width="339" data-align="center">

- Le premier Raspberry sera monté dans le robot.

- le deuxième quant à lui vous servira afin de développer le code du robot (vous pouvez aussi utiliser votre propre PC). Il pourra aussi servir de télécommande afin de contrôler le robot par la suite.

Il vous sera aussi fourni un kit Rasptank, ce kit inclut toutes les pièces permettant de construire un petit robot sur chenille téléguidé.

<img title="" src="images/rasptank.png" alt="" width="327" data-align="center">

## Objectifs

La séance d'évaluation sera une partie de *World of Rasptank*, il est donc impératif que vous ayez un robot opérationnelle à la dernière séance. Voici une liste exhaustive de tous ce que vous devez implémenter afin que votre robot puisse participer à une partie de  *World of Rasptank* : 

#### Rasptank

* Recevoir des commandes de la télécommande
- Se déplacer dans toutes les directions

- Tirer via l'émetteur infrarouge

- Recevoir les tirs via le récepteur infrarouge

- Détecter quand il entre dans la zone de capture (zone blanche) via le module suiveur de ligne

- Streamer en temps réelle le flux vidéo issu de la webcam

#### Télécommande

Ici vous êtes libres de faire ce que vous voulez, votre télécommande doit cependant permettre 2 choses:

- Envoyer des commandes au Rasptank (déplacement, tirs, ...)

- Visualiser le stream de la webcam

<img title="" src="images/controller_tk.png" alt="" width="555" data-align="center">

### Informations liées à la documentation

Vous trouverez sur le Git des guides pour chaque partie du projet. Dans ces guides vous trouverez des explications concernant le code fournis ou des pistes pour les fonctionnalités à implémenter. 

Toutes les options présentées sont bonnes et vous pouvez choisir celle qui vous plait le plus, ou même quelque chose qui n'est pas présenté dans le guide si vous le souhaitez. 

Les choix d'implémentation que j'ai fait lors de la conception de ce projet sont notés par une :star:. Si vous n'avez pas de préférence quant à la manière d'implémenter une fonctionnalité, je vous conseille de choisir l'option :star:, je pourrais ainsi plus facilement vous aider si vous avez un problème.
