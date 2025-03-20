# Installation de Mosquitto

Ce guide vous montre comment installer un broker MQTT en local afin que vous puissiez travailler depuis chez vous.

## Installation complète

Mettez à jour la liste des paquets :

```bash
sudo apt update
```

Installez Mosquitto :

```bash
sudo apt install mosquitto
```

Récupérez l'adresse IP de votre laptop :

```bash
ifconfig
```

![Illustration ifconfig](/documentation/images/ifconfig.png)

Édition de la configuration du broker :

```bash
sudo nano /etc/mosquitto/mosquitto.conf
```

Ajoutez à la fin du fichier `mosquitto.conf` les lignes suivantes (remplacez `<ip de votre laptop>` par votre adresse IP réelle, sans les `< >`) :

```bash
allow_anonymous true
listener 1883 <ip de votre laptop>
```

Redémarrez Mosquitto :

```bash
sudo systemctl restart mosquitto.service
```

Ouvrez le port 1883 sur votre laptop :

```bash
sudo iptables -A INPUT -p udp --dport 1883 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 1883 -j ACCEPT
```

### Pour rendre les modifications du pare-feu permanentes

Sauvegardez les règles :

```bash
sudo netfilter-persistent save
```

Si nécessaire, installez `iptables-persistent` :

```bash
sudo apt-get install iptables-persistent
```

## Erreurs

:warning: Utilisez l'autocomplétion avec la touche Tab.

Si vous rencontrez une erreur de type "permission denied" ou quelque chose de similaire, réexécutez les commandes iptables:

```bash
sudo iptables -A INPUT -p udp --dport 1883 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 1883 -j ACCEPT
```