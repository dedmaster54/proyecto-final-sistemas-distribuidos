import os
import requests

LOCAL_API = "http://localhost:5000"           # Dirección de este nodo
FRAGMENTS_DIR = "fragments"

def listar_fragmentos_remoto(remote_url):
    """Consulta qué fragmentos tiene el otro nodo"""
    try:
        r = requests.get(f"{remote_url}/fragmentos")
        return r.json()
    except Exception as e:
        print(f" Error al conectar a {remote_url}: {e}")
        return []

def obtener_fragmento(remote_url, fragment_name):
    """Descarga un fragmento específico desde otro nodo"""
    url = f"{remote_url}/fragmentos/{fragment_name}"
    r = requests.get(url)
    if r.status_code == 200:
        path = os.path.join(FRAGMENTS_DIR, fragment_name)
        with open(path, 'wb') as f:
            f.write(r.content)
        print(f" Fragmento {fragment_name} guardado")
        return True
    else:
        print(f" Fragmento {fragment_name} no disponible en {remote_url}")
        return False

def registrar_local(fragment_name):
    """Llama al endpoint local para registrar un fragmento"""
    r = requests.post(f"{LOCAL_API}/registrar", data={'filename': fragment_name})
    if r.status_code == 200:
        print(f"Fragmento {fragment_name} registrado localmente")
    else:
        print(f"Error al registrar fragmento: {r.text}")

def obtener_fragmentos_faltantes(remote_url):
    """Obtiene fragmentos del nodo remoto que este nodo no tiene"""
    remote_fragments = listar_fragmentos_remoto(remote_url)

    local_response = requests.get(f"{LOCAL_API}/fragmentos")
    local_fragments = local_response.json()

    faltantes = list(set(remote_fragments) - set(local_fragments))
    print(f" Fragmentos faltantes: {faltantes}")

    for frag in faltantes:
        if obtener_fragmento(remote_url, frag):
            registrar_local(frag)

if __name__ == "__main__":
    print(" Cliente P2P iniciado")
    remote_ip = input("Ingresa IP del nodo remoto (ej. http://localhost:5001): ")
    obtener_fragmentos_faltantes(remote_ip)
