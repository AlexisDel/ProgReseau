# Installation de Tailscale :

1) Créez un compte Tailscale : [https://login.tailscale.com/start](https://login.tailscale.com/start)

2) Installez Tailscale sur votre PC : [https://tailscale.com/download](https://tailscale.com/download)

3) Installez Tailscale sur votre robot et récupérez son adresse IP :

```bash
sudo apt update
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
tailscale ip -4
```

4) Connectez-vous à votre robot en SSH via l'IP obtenue.

Votre robot et votre PC sont maintenant connectés sur le même VPN (Virtual Private Network). Vous pouvez donc accéder à votre robot via l'adresse IP donnée par Tailscale, même s'il se trouve chez votre binôme (à condition qu'il soit allumé, bien sûr).

Pour que votre binôme ait accès au robot, il doit lui aussi créer un compte Tailscale et installer l'application. Vous devrez ensuite partager le raspberry avec lui. Voir : [https://tailscale.com/kb/1084/sharing](https://tailscale.com/kb/1084/sharing)

:warning: Il existe une option SSH « intégrée » à Tailscale, activable via la commande `tailscale up --ssh`. Il NE FAUT PAS l’activer !


**Référence** : [https://tailscale.com/learn/how-to-ssh-into-a-raspberry-pi](https://tailscale.com/learn/how-to-ssh-into-a-raspberry-pi)