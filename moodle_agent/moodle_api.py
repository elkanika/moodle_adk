# moodle_agent/moodle_api.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class MoodleAPI:
    def __init__(self):
        self.moodle_api_url = os.environ.get("MOODLE_URL")
        self.moodle_url_base = self.moodle_api_url.replace("/webservice/rest/server.php", "")
        self.admin_username = os.environ.get("ADMIN_USERNAME")
        self.admin_password = os.environ.get("ADMIN_PASSWORD")
        self.service_shortname = os.environ.get("MOODLE_SERVICE_SHORTNAME")
        self.token_cache = None

    def get_admin_token(self):
        if self.token_cache:
            return self.token_cache
        
        token_url = f"{self.moodle_url_base}/login/token.php"
        params = {
            'username': self.admin_username,
            'password': self.admin_password,
            'service': self.service_shortname,
            'moodlewsrestformat': 'json'
        }
        try:
            # ¡QUITAR verify=False EN PRODUCCIÓN!
            response = requests.post(token_url, data=params, verify=False)
            response.raise_for_status()
            data = response.json()
            if 'token' in data:
                self.token_cache = data['token']
                print("ADMIN_AUTH: Token obtenido exitosamente.")
                return self.token_cache
            else:
                print(f"ADMIN_AUTH: Error al obtener token: {data}")
                return None
        except Exception as e:
            print(f"ADMIN_AUTH: Excepción crítica al obtener token: {e}")
            return None

    def call(self, wsfunction, params=None):
        token = self.get_admin_token()
        if not token:
            return {"error": "Token de Moodle (admin) no disponible."}
        
        payload = {'wstoken': token, 'wsfunction': wsfunction, 'moodlewsrestformat': 'json'}
        if params:
            payload.update(params)
        
        try:
            # ¡QUITAR verify=False EN PRODUCCIÓN!
            response = requests.post(self.moodle_api_url, data=payload, verify=False)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error en llamada a API Moodle ({wsfunction}): {e}")
            return {"exception": "api_call_failed", "message": str(e)}

# Instancia única para ser usada por las herramientas
moodle_client = MoodleAPI()