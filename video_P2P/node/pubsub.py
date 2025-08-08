import requests
import os

FRAGMENTS_DIR = "fragments"

# Lista de suscriptores (URLs base de otros nodos)
subscribers = set()

def add_subscriber(url):
    subscribers.add(url)
    print(f" Nodo suscrito: {url}")

def notify_subscribers(fragment_name, sender_url):
    """Notifica a todos los suscriptores con el nombre del fragmento y URL de origen"""
    for sub in subscribers:
        try:
            print(f" Notificando a {sub} sobre fragmento {fragment_name}")
            requests.post(
                f"{sub}/registrar",
                data={"filename": fragment_name, "source_url": sender_url}
            )
        except Exception as e:
            print(f" No se pudo notificar a {sub}: {e}")

def descargar_fragmento(source_url, fragment_name):
    """Descarga un fragmento desde el nodo de origen"""
    try:
        r = requests.get(f"{source_url}/fragmentos/{fragment_name}")
        if r.status_code == 200:
            path = os.path.join(FRAGMENTS_DIR, fragment_name)
            with open(path, 'wb') as f:
                f.write(r.content)
            print(f" Fragmento {fragment_name} descargado desde {source_url}")
            return True
        else:
            print(f" No se pudo descargar {fragment_name} desde {source_url}")
            return False
    except Exception as e:
        print(f" Error al descargar: {e}")
        return False
