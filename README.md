# Building environment

## docker

```sh
docker-compose up --build
```

## Synchronize the local and docker environment

```sh
cd project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
