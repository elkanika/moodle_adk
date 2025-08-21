Agente de Moodle con ADK y Ollama (o gemini)
Este proyecto implementa un agente de inteligencia artificial utilizando el Agent Development Kit (ADK) de Google para realizar tareas administrativas en una plataforma Moodle. El agente es capaz de entender peticiones en lenguaje natural y traducirlas en acciones concretas a través de los servicios web de Moodle.

Para el procesamiento del lenguaje, el agente se conecta a un servidor local de Ollama, lo que permite utilizar modelos de lenguaje de código abierto como phi3 de forma completamente privada y sin conexión a internet.

🚀 Características Principales
El agente está equipado con un conjunto de herramientas para gestionar las áreas más comunes de Moodle:

Gestión de Usuarios:

Crear, listar, actualizar y eliminar usuarios.

Obtener información detallada de un usuario específico.

Buscar usuarios por nombre y manejar resultados ambiguos.

Gestión de Cursos:

Listar todos los cursos disponibles.

Crear nuevos cursos.

Obtener la lista completa de participantes de un curso.

Inscripciones y Calificaciones:

Inscribir (matricular) usuarios en cursos con roles de "profesor" o "estudiante".

Obtener un resumen de las calificaciones de un usuario.

🛠️ Tecnologías Utilizadas
Python 3.11+

Google Agent Development Kit (ADK): Framework para la construcción del agente.

Ollama: Para servir modelos de lenguaje locales (ej. phi3, gemma:2b).

Moodle Web Services: Para la interacción con la plataforma Moodle.

Bibliotecas de Python: httpx, requests, python-dotenv.

📋 Prerrequisitos
Antes de empezar, asegúrate de tener instalado lo siguiente:

Python 3.11 o superior.

Git.

Ollama: Descárgalo e instálalo desde ollama.com.

Un modelo de lenguaje local: Se recomienda phi3 por su balance entre rendimiento y consumo de recursos.

Bash

ollama pull phi3
Una instancia de Moodle con los servicios web habilitados (Administración del sitio > Avanzado > Habilitar servicios web).

⚙️ Instalación y Configuración
Sigue estos pasos para poner en marcha el agente en tu máquina local.

1. Clonar el Repositorio:

Bash

git clone https://github.com/elkanika/moodle_adk.git
cd moodle_adk
2. Crear y Activar un Entorno Virtual:

Bash

# Crear el entorno
python -m venv venv

# Activar en Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Activar en macOS/Linux
source venv/bin/activate
3. Instalar las Dependencias:
Con el entorno virtual activo, instala todas las librerías necesarias.

Bash

pip install -r requirements.txt
4. Configurar las Variables de Entorno:
Crea una copia del archivo de ejemplo .env.example y renómbrala a .env.

Bash

# En Windows
copy .env.example .env

# En macOS/Linux
cp .env.example .env
Luego, abre el archivo .env y rellena los valores con tus propias credenciales de Moodle.

Fragmento de código

# Credenciales de la API de Moodle
MOODLE_URL="https://tu_moodle/webservice/rest/server.php"
ADMIN_USERNAME="tu_usuario_admin"
ADMIN_PASSWORD="tu_contraseña_admin"
MOODLE_SERVICE_SHORTNAME="nombre_del_servicio_moodle"

# Credenciales de la API de Google (no necesaria si usas solo Ollama)
GOOGLE_API_KEY=""
▶️ Ejecución
Para iniciar el agente y su interfaz web, asegúrate de que Ollama esté corriendo en segundo plano.

Luego, con el entorno virtual activo, ejecuta el siguiente comando desde la carpeta raíz del proyecto:

Bash

adk web .
El servidor se iniciará. Abre tu navegador y ve a la dirección que te indica la terminal (usualmente http://localhost:8000). En la interfaz web, selecciona moodle_agent en el menú desplegable y comienza a chatear.
