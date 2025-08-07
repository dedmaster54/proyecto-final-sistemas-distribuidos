import os
from flask import Flask, jsonify, send_from_directory, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

FRAGMENTS_DIR = 'fragments'
available_fragments = set()  # Lista en memoria

# Cargar fragmentos existentes al iniciar
if os.path.exists(FRAGMENTS_DIR):
    available_fragments = set(os.listdir(FRAGMENTS_DIR))
else:
    os.makedirs(FRAGMENTS_DIR)

@app.route('/fragmentos', methods=['GET'])
def listar_fragmentos():
    """
    Lista los fragmentos disponibles
    ---
    responses:
      200:
        description: Lista de fragmentos
    """
    return jsonify(sorted(list(available_fragments)))

@app.route('/fragmentos/<filename>', methods=['GET'])
def obtener_fragmento(filename):
    """
    Descargar un fragmento específico
    ---
    parameters:
      - name: filename
        in: path
        type: string
        required: true
    responses:
      200:
        description: Fragmento enviado
      404:
        description: No encontrado
    """
    if filename not in available_fragments:
        return jsonify({"error": "Fragmento no disponible"}), 404
    return send_from_directory(FRAGMENTS_DIR, filename)

@app.route('/registrar', methods=['POST'])
def registrar_fragmento():
    """
    Registrar nuevo fragmento recibido
    ---
    parameters:
      - name: filename
        in: formData
        type: string
        required: true
    responses:
      200:
        description: Registro exitoso
    """
    filename = request.form.get('filename')
    if not filename:
        return jsonify({"error": "Falta 'filename'"}), 400

    available_fragments.add(filename)
    # Aquí luego notificaríamos al pub/sub (más adelante)
    print(f" Fragmento registrado: {filename}")
    return jsonify({"mensaje": f"{filename} registrado correctamente"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
