import os
from flask import Flask, jsonify, send_from_directory, request
from flasgger import Swagger
from pubsub import notify_subscribers, add_subscriber, descargar_fragmento

app = Flask(__name__)
Swagger(app)

# Config desde entorno (para docker)
PORT = int(os.environ.get("PORT", "5000"))
PUBLIC_URL = os.environ.get("PUBLIC_URL", f"http://localhost:{PORT}")
FRAGMENTS_DIR = os.environ.get("FRAGMENTS_DIR", "fragments")

if not os.path.exists(FRAGMENTS_DIR):
    os.makedirs(FRAGMENTS_DIR)

# available_fragments en memoria (nombre de archivos)
available_fragments = set(os.listdir(FRAGMENTS_DIR))

@app.route('/fragmentos', methods=['GET'])
def listar_fragmentos():
    return jsonify(sorted(list(available_fragments)))

@app.route('/fragmentos/<filename>', methods=['GET'])
def obtener_fragmento(filename):
    if filename not in available_fragments:
        return jsonify({"error": "Fragmento no disponible"}), 404
    return send_from_directory(FRAGMENTS_DIR, filename, as_attachment=True)

@app.route('/registrar', methods=['POST'])
def registrar_fragmento():
    filename = request.form.get('filename')
    source_url = request.form.get('source_url')

    if not filename:
        return jsonify({"error": "Falta 'filename'"}), 400

    if filename in available_fragments:
        return jsonify({"mensaje": f"{filename} ya registrado"}), 200

    # Si viene con source_url -> descargar
    if source_url:
        exito = descargar_fragmento(source_url, filename)
        if not exito:
            return jsonify({"error": "No se pudo descargar el fragmento"}), 500

    # Registrar en memoria
    available_fragments.add(filename)
    print(f"📥 Fragmento registrado: {filename}")

    # Si es registro local (sin source_url), notificar a suscriptores
    if not source_url:
        # usar PUBLIC_URL para que los demás puedan llegar a este nodo
        notify_subscribers(filename, PUBLIC_URL)

    return jsonify({"mensaje": f"{filename} registrado correctamente"}), 200

@app.route('/suscribir', methods=['POST'])
def suscribir_nodo():
    node_url = request.form.get('url')
    if not node_url:
        return jsonify({"error": "Falta 'url'"}), 400
    add_subscriber(node_url)
    return jsonify({"mensaje": f"{node_url} suscrito correctamente"}), 200

if __name__ == '__main__':
    # Flask debug false en producción; aquí lo dejamos simple para pruebas
    app.run(host='0.0.0.0', port=PORT)
