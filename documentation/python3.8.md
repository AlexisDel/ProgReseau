# Installer Python 3.8 sur Debian 13 avec pyenv


## 1) Installer les dépendances
```
sudo apt update
sudo apt install -y build-essential curl git ca-certificates \
  libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev \
  libffi-dev liblzma-dev tk-dev xz-utils libncursesw5-dev
```

## 2) Installer pyenv

```bash
curl https://pyenv.run | bash
```

Ajouter à `~/.bashrc` ou `~/.zshrc` :

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

Recharger le shell :

```bash
source ~/.bashrc   # ou ~/.zshrc
```

## 3) Installer Python 3.8

```bash
pyenv install 3.8.20
```

## 4) Créer un virtual environment

```bash
pyenv shell 3.8.20
python -m venv ~/venvs/py38
source ~/venvs/py38/bin/activate
```

## 5) Vérifier

```bash
python --version
which python
```
