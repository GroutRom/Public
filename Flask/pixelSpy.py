import requests
from flask import Flask, request, send_file, Response
import io
import base64
import logging

app = Flask(__name__)

# Un pixel transparent (1x1 px) en base64
pixel_data = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wcAAwAB/eqHQlsAAAAASUVORK5CYII="
)

logging.basicConfig(filename='tracking.log', level=logging.INFO)

@app.route('/pixel.png')
def pixel():
    user_ip = request.remote_addr

    # Obtenir la localisation via l'API ip-api
    try:
        response = requests.get(f'http://ip-api.com/json/{user_ip}')
        data = response.json()
        if data['status'] == 'success':
            location_info = f"{data['city']}, {data['country']}"
        else:
            location_info = "Unknown"
    except Exception as e:
        location_info = "Unknown"

    # Enregistrer les données de suivi dans les logs
    logging.info(f"IP: {user_ip}, Location: {location_info}, User-Agent: {request.headers.get('User-Agent')}")

    # Retourner un pixel transparent
    return Response(pixel_data, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)